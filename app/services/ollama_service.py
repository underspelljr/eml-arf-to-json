import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import ollama
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)

# Define the path to the labeling guide
GUIDE_PATH = Path("labeling_guide.md")


@lru_cache(maxsize=1)
def get_system_prompt() -> str:
    """
    Loads the labeling guide content to be used as the system prompt.
    Uses lru_cache to read the file only once.
    """
    try:
        logger.info("Loading labeling guide from '%s' for system prompt.", GUIDE_PATH)
        with open(GUIDE_PATH, "r", encoding="utf-8") as f:
            guide_content = f.read()

        prompt = f"""
You are a senior cybersecurity analyst specializing in email threat detection.
Your task is to analyze a JSON representation of an email and determine its category based on the detailed guidelines provided below.
You must return your analysis in a structured JSON format.

The JSON output MUST contain the following keys:
- "verdict": One of "Malicious", "Spam", "Graymail", "Benign", or "Unknown".
- "category": The specific subcategory from the guidelines (e.g., "Credential Harvesting (Phishing)", "Lead Generation/Contact List Solicitation").
- "reason": A brief, clear explanation for your verdict, referencing specific evidence from the email JSON.
- "rules": A list of simple, actionable detection rules based on your analysis. Each rule should be a JSON object with "type" and "value" keys. Examples: {{"type": "subject_keyword", "value": "urgent payment"}}, {{"type": "domain_reputation", "value": "suspicious-site.com"}}.

--- START OF GUIDELINES ---
{guide_content}
--- END OF GUIDELINES ---

Now, analyze the following email JSON and provide your response in the specified JSON format only. Do not add any extra text or explanations outside of the JSON structure.
"""
        logger.info("System prompt loaded successfully.")
        return prompt
    except FileNotFoundError:
        logger.error("CRITICAL: The labeling guide at '%s' was not found.", GUIDE_PATH)
        raise RuntimeError(f"Labeling guide not found at {GUIDE_PATH.absolute()}")


async def generate_rules_for_eml(
    parsed_eml_json: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Sends the parsed EML JSON to Ollama to generate a security analysis.
    """
    system_prompt = get_system_prompt()
    user_prompt = json.dumps(parsed_eml_json, indent=2)

    logger.debug(
        "Sending request to Ollama model '%s' at host '%s'.",
        settings.OLLAMA_MODEL,
        settings.OLLAMA_HOST,
    )

    try:
        client = ollama.AsyncClient(host=settings.OLLAMA_HOST)
        response = await client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format="json",  # Instruct Ollama to ensure the output is valid JSON
        )

        content = response["message"]["content"]
        logger.debug("Received raw response from Ollama.")

        # The 'format="json"' parameter should ensure this is valid JSON
        analysis_json = json.loads(content)
        return analysis_json

    except json.JSONDecodeError as e:
        logger.error(
            "Failed to decode JSON response from Ollama: %s. Response content: %s",
            e,
            content,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse analysis from the AI model.",
        )
    except Exception as e:
        logger.error(
            "An error occurred while communicating with Ollama: %s", e, exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not communicate with the analysis service: {e}",
        )

