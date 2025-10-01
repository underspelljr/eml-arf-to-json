import json
import logging
from typing import Any, Dict

from eml_parser import EmlParser

logger = logging.getLogger(__name__)


def parse_eml_content(eml_bytes: bytes) -> Dict[str, Any]:
    """
    Parses the raw byte content of an EML file.

    This service uses the `eml-parser` library to extract structured
    data from an EML file.

    Args:
        eml_bytes: The byte content of the .eml file.

    Returns:
        A dictionary containing the parsed email data.
    """
    logger.debug("Initializing EML parser.")
    ep = EmlParser(
        include_raw_body=True, include_attachment_data=False
    )
    
    try:
        logger.debug("Attempting to parse EML content.")
        # The library expects a JSON string, so we decode bytes if necessary,
        # but it can often handle bytes directly. Let's try parsing directly.
        # The library's `decode` method handles the heavy lifting.
        parsed_eml = ep.decode_email_bytes(eml_bytes)
        logger.info("EML content parsed successfully.")

        # The output can contain non-serializable types like datetime.
        # The library author suggests using json.dumps with a default handler.
        def json_default_serializer(o):
            if hasattr(o, "isoformat"):
                return o.isoformat()
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

        # To ensure the final output is a clean dictionary, we serialize and then deserialize.
        # This is a robust way to handle any complex objects from the parser.
        eml_json_str = json.dumps(parsed_eml, default=json_default_serializer)
        clean_dict = json.loads(eml_json_str)

        logger.debug("EML data serialized and cleaned successfully.")
        return clean_dict

    except Exception as e:
        logger.error("An exception occurred during EML parsing: %s", e, exc_info=True)
        # Re-raise the exception to be handled by the API endpoint
        raise
