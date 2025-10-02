import logging

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.rule_generation import RuleGenerationResponse
from app.services.ollama_service import generate_rules_for_eml
from app.services.parser_service import parse_eml_content

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/generate_from_file",
    response_model=RuleGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse an EML file and generate detection rules",
    description="Upload an email file (.eml or .arf) to parse it and then use an LLM to generate detection rules based on its content.",
)
async def generate_rules_from_eml_file(
    file: UploadFile = File(
        ..., description="The .eml or .arf file to be analyzed."
    )
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

        # Step 1: Parse the EML file content
        parsed_data = parse_eml_content(content)
        logger.info("Successfully parsed file '%s'.", file.filename)

        # Step 2: Generate rules using the Ollama service
        analysis_result = await generate_rules_for_eml(parsed_data)
        logger.info(
            "Successfully generated rules for file '%s'.", file.filename
        )

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

