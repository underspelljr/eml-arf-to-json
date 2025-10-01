import os
from pathlib import Path

import pytest

from app.services.parser_service import parse_eml_content

# Define the path to the sample EML file
# This assumes the tests are run from the project root directory
SAMPLE_EML_PATH = Path(__file__).parent.parent / "sample_data" / "sample.eml"


@pytest.fixture(scope="module")
def sample_eml_content() -> bytes:
    """
    Reads and returns the content of the sample.eml file.
    """
    # Create a dummy EML file for testing
    eml_data = b"""From: sender@example.com
To: receiver@example.com
Subject: Test EML

This is the body of the test email.
"""
    SAMPLE_EML_PATH.parent.mkdir(exist_ok=True)
    with open(SAMPLE_EML_PATH, "wb") as f:
        f.write(eml_data)
    
    with open(SAMPLE_EML_PATH, "rb") as f:
        return f.read()


def test_parse_eml_content_success(sample_eml_content):
    """
    Test that the parser service successfully parses a valid EML file.
    """
    parsed_data = parse_eml_content(sample_eml_content)

    assert isinstance(parsed_data, dict)
    assert "header" in parsed_data
    assert "body" in parsed_data
    assert parsed_data["header"]["subject"] == "Test EML"
    assert parsed_data["header"]["from"] == "sender@example.com"
    assert "receiver@example.com" in parsed_data["header"]["to"]


def test_parse_eml_content_invalid_input():
    """
    Test that the parser service raises an exception for invalid input.
    """
    invalid_content = b"this is not a valid eml file"
    parsed_data = parse_eml_content(invalid_content)
    assert "defect" in parsed_data["header"]