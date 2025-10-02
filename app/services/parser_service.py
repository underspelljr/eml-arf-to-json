import json
import logging
import datetime
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
        parsed_eml = ep.decode_email_bytes(eml_bytes)
        logger.info("EML content parsed successfully.")

        def json_default_serializer(o):
            if hasattr(o, "isoformat"):
                return o.isoformat()
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

        eml_json_str = json.dumps(parsed_eml, default=json_default_serializer)
        clean_dict = json.loads(eml_json_str)

        logger.debug("EML data serialized and cleaned successfully.")
        return clean_dict

    except Exception as e:
        logger.error("An exception occurred during EML parsing: %s", e, exc_info=True)
        # Re-raise the exception to be handled by the API endpoint
        raise
