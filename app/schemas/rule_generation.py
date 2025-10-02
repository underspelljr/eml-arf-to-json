from typing import Any, Dict, List, Literal

from pydantic import BaseModel

Verdict = Literal["Malicious", "Spam", "Graymail", "Benign", "Unknown"]


class DetectionRule(BaseModel):
    """
    Represents a single, simple detection rule.
    """

    type: str
    value: Any


class RuleGenerationResponse(BaseModel):
    """
    Defines the structured response from the AI analysis.
    """

    verdict: Verdict
    category: str
    reason: str
    rules: List[DetectionRule]

