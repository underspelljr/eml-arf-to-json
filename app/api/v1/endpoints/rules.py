import datetime
import json
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.email import ParsedEmail, RawEmail
from app.schemas.rule_generation import RuleGenerationResponse
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
    "/generate_from_file",
    status_code=status.HTTP_200_OK,
    summary="Parse an EML file and generate detection rules",
    description="Upload an email file (.eml or .arf) to parse it and then use an LLM to generate detection rules based on its content.",
)
async def generate_rules_from_eml_file(
    file: UploadFile = File(
        ..., description="The .eml or .arf file to be analyzed."
    ),
    db: Session = Depends(get_db)
):
    """
    Parses an uploaded EML file, sends the structured data to Ollama
    for analysis, and returns generated detection rules.
    """
    logger.info("Received file '%s' for rule generation.", file.filename)

    if not (
        file.filename.lower().endswith(".eml")
        or file.filename.lower().endswith(".arf")
    ):
        logger.warning(
            "Invalid file extension for rule generation on file '%s'.",
            file.filename,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a .eml or .arf file.",
        )

    try:
        content = await file.read()
        logger.debug(
            "Read %d bytes from '%s' for parsing.", len(content), file.filename
        )

        # Save raw email content
        raw_email_entry = RawEmail(raw_content=content.decode('utf-8', errors='ignore').replace('\x00', ''))
        db.add(raw_email_entry)
        db.commit()
        db.refresh(raw_email_entry)
        logger.info("Raw EML content saved to database with ID: %s", raw_email_entry.id)

        # Step 1: Parse the EML file content
        parsed_data = parse_eml_content(content)
        logger.info("Successfully parsed file '%s'.", file.filename)

        # Step 2: Generate rules using the Ollama service
        try:
            analysis_result = await generate_rules_for_eml(parsed_data)
            logger.info(
                "Successfully generated rules for file '%s'.", file.filename
            )
        except Exception as ollama_exc:
            logger.error("Ollama analysis failed: %s", ollama_exc, exc_info=True)
            analysis_result = {"error": "Ollama analysis failed", "details": str(ollama_exc)}

        # Extract fields for parsed_emails table
        from_address_list = parsed_data.get("header", {}).get("from", [""])
        from_address = ", ".join(from_address_list) if isinstance(from_address_list, list) else from_address_list
        to_address = parsed_data.get("header", {}).get("to", [""])[0]
        subject_list = parsed_data.get("header", {}).get("subject", [""])
        subject = ", ".join(subject_list) if isinstance(subject_list, list) else subject_list
        date_str = parsed_data.get("header", {}).get("date", [""])[0]
        # Attempt to parse date, default to current UTC if parsing fails
        try:
            date_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            date_obj = datetime.datetime.utcnow()

        sender_ip = parsed_data.get("header", {}).get("received_ip", [""])[0]

        # Save parsed data to database
        parsed_email_entry = ParsedEmail(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            date=date_obj,
            sender_ip=sender_ip,
            ollama_evaluation=json.dumps(analysis_result), # Store as JSON string
        )
        raw_email_entry.parsed_email = parsed_email_entry
        db.add(parsed_email_entry)
        db.add(raw_email_entry)
        db.commit()
        db.refresh(parsed_email_entry)
        db.refresh(raw_email_entry)
        logger.info("Parsed EML data saved to database with ID: %s", parsed_email_entry.id)

        return analysis_result

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions from services
        raise http_exc
    except Exception as e:
        logger.error(
            "Failed to generate rules for file '%s': %s",
            file.filename,
            e,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )
    finally:
        await file.close()

