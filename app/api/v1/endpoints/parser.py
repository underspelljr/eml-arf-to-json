import datetime
import json
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.email import ParsedEmail, RawEmail
from app.services.ollama_service import generate_rules_for_eml
from app.services.parser_service import parse_eml_content

router = APIRouter()
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/parse_message",
    status_code=status.HTTP_200_OK,
    summary="Parse an EML or ARF file",
    description="Upload an email file (.eml or .arf) to parse its headers, body, and attachments.",
)
async def parse_message_file(
    file: UploadFile = File(
        ..., description="The .eml or .arf file to be parsed."
    ),
    db: Session = Depends(get_db)
):
    logger.info("Received file '%s' for parsing.", file.filename)

    if not (
        file.filename.lower().endswith(".eml")
        or file.filename.lower().endswith(".arf")
    ):
        logger.warning(
            "Invalid file extension for file '%s'.", file.filename
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a .eml or .arf file.",
        )

    try:
        content = await file.read()
        logger.debug("Successfully read %d bytes from '%s'.", len(content), file.filename)
        
        # Save raw email content
        raw_email_entry = RawEmail(raw_content=content.decode('utf-8', errors='ignore').replace('\x00', ''))
        db.add(raw_email_entry)
        db.commit()
        db.refresh(raw_email_entry)
        logger.info("Raw EML content saved to database with ID: %s", raw_email_entry.id)

        # Parse the EML content to get a structured dictionary
        parsed_data_for_ollama = parse_eml_content(content)

        # Then, send the parsed data to Ollama for evaluation
        ollama_evaluation = await generate_rules_for_eml(parsed_data_for_ollama)

        # Extract fields for parsed_emails table
        from_address_list = parsed_data_for_ollama.get("header", {}).get("from", [""])
        from_address = ", ".join(from_address_list) if isinstance(from_address_list, list) else from_address_list
        to_address = parsed_data_for_ollama.get("header", {}).get("to", [""])[0]
        subject_list = parsed_data_for_ollama.get("header", {}).get("subject", [""])
        subject = ", ".join(subject_list) if isinstance(subject_list, list) else subject_list
        date_str = parsed_data_for_ollama.get("header", {}).get("date", [""])[0]
        # Attempt to parse date, default to current UTC if parsing fails
        try:
            date_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            date_obj = datetime.datetime.utcnow()

        sender_ip = parsed_data_for_ollama.get("header", {}).get("received_ip", [""])[0]

        # Save parsed data to database
        parsed_email_entry = ParsedEmail(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            date=date_obj,
            sender_ip=sender_ip,
            ollama_evaluation=json.dumps(ollama_evaluation), # Store as JSON string
        )
        raw_email_entry.parsed_email = parsed_email_entry
        db.add(parsed_email_entry)
        db.add(raw_email_entry)
        db.commit()
        db.refresh(parsed_email_entry)
        db.refresh(raw_email_entry)
        logger.info("Parsed EML data saved to database with ID: %s", parsed_email_entry.id)

        return parsed_data_for_ollama
    except Exception as e:
        logger.error(
            "Failed to parse file '%s': %s", file.filename, e, exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while parsing the file: {e}",
        )
    finally:
        await file.close()


from app.schemas.visualization import VisualizationData

@router.get("/get", response_model=VisualizationData)
async def get_visualization_data(db: Session = Depends(get_db)):
    """
    Retrieve all data from both tables for visualization.
    """
    parsed_emails_db = db.query(ParsedEmail).all()
    parsed_emails_response = []
    for email in parsed_emails_db:
        parsed_emails_response.append({
            "id": email.id,
            "from_address": email.from_address,
            "to_address": email.to_address,
            "subject": email.subject,
            "date": email.date,
            "sender_ip": email.sender_ip,
            "ollama_evaluation": email.ollama_evaluation,
            "raw_email_id": email.raw_email.id if email.raw_email else None,
        })
    raw_emails = db.query(RawEmail).filter(RawEmail.parsed_email_id != None).all()
    return {"parsed_emails": parsed_emails_response, "raw_emails": raw_emails}


@router.get("/emails", response_model=list[dict])
async def get_all_emails(db: Session = Depends(get_db)):
    """
    Retrieve all parsed emails from the database.
    """
    emails = db.query(ParsedEmail).all()
    return [
        {
            "id": email.id,
            "from_address": email.from_address,
            "to_address": email.to_address,
            "subject": email.subject,
            "date": email.date.isoformat(),
            "sender_ip": email.sender_ip,
            "ollama_evaluation": json.loads(email.ollama_evaluation) if email.ollama_evaluation else None,
            "raw_email_id": email.raw_email.id if email.raw_email else None,
        }
        for email in emails
    ]


@router.delete("/emails/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email(email_id: int, db: Session = Depends(get_db)):
    """
    Delete a parsed email and its associated raw email content from the database.
    """
    parsed_email = db.query(ParsedEmail).filter(ParsedEmail.id == email_id).first()
    if not parsed_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with ID {email_id} not found."
        )

    # Delete associated raw email first
    if parsed_email.raw_email:
        db.delete(parsed_email.raw_email)

    db.delete(parsed_email)
    db.commit()
    logger.info("Email with ID %s and its raw content deleted successfully.", email_id)
    return
