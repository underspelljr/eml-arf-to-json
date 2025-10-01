import logging

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.parser_service import parse_eml_content

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/parse_message",
    status_code=status.HTTP_200_OK,
    summary="Parse an EML or ARF file",
    description="Upload an email file (.eml or .arf) to parse its headers, body, and attachments.",
)
async def parse_message_file(
    file: UploadFile = File(
        ..., description="The .eml or .arf file to be parsed."
    )
):
    """
    Parses an uploaded EML file and returns its structured content.

    The file content is read and passed to the parsing service.
    - **file**: The uploaded file in `multipart/form-data` format.
    """
    logger.info("Received file '%s' for parsing.", file.filename)

    # Basic validation for file extension
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
        
        parsed_data = parse_eml_content(content)
        
        logger.info("Successfully parsed file '%s'.", file.filename)
        return parsed_data
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
