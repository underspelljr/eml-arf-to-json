from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Path to the sample EML file for testing uploads
SAMPLE_EML_PATH = Path(__file__).parent.parent / "sample_data" / "sample.eml"

def test_read_root(test_client: TestClient):
    """
    Test the root endpoint.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert "Welcome" in json_response["message"]


def test_get_app_status(test_client: TestClient):
    """
    Test the /app_status endpoint.
    """
    response = test_client.get("/api/v1/app_status")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "ok"
    assert "name" in json_response
    assert "version" in json_response


def test_parse_message_file_success(test_client: TestClient):
    """
    Test the /parse_message endpoint with a valid EML file.
    """
    # Ensure the sample file exists
    if not SAMPLE_EML_PATH.exists():
        SAMPLE_EML_PATH.parent.mkdir(exist_ok=True)
        SAMPLE_EML_PATH.write_text("Subject: Test\n\nHello World")

    with open(SAMPLE_EML_PATH, "rb") as f:
        files = {"file": ("sample.eml", f, "message/rfc822")}
        response = test_client.post("/api/v1/parse_message", files=files)

    assert response.status_code == 200
    json_response = response.json()
    assert "header" in json_response
    assert "body" in json_response
    assert json_response["header"]["subject"] == "Test"


def test_parse_message_file_invalid_extension(test_client: TestClient):
    """
    Test the /parse_message endpoint with a file that has an invalid extension.
    """
    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = test_client.post("/api/v1/parse_message", files=files)

    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_generate_rules_from_file_success(test_client: TestClient, mocker):
    """
    Test the /rules/generate_from_file endpoint, mocking the Ollama call.
    """
    # Mock the ollama.chat function
    mock_ollama_chat = mocker.patch(
        "app.services.ollama_service.ollama.chat",
        return_value={
            "message": {
                "content": '''
                {
                    "verdict": "Malicious",
                    "category": "Credential Harvesting (Phishing)",
                    "reason": "The email contains a suspicious link with a call-to-action to verify account details, which is a common phishing tactic.",
                    "rules": [
                        { "type": "keyword", "value": "verify your account" },
                        { "type": "domain_reputation", "value": "suspicious-login.com" }
                    ]
                }
                '''
            }
        }
    )

    with open(SAMPLE_EML_PATH, "rb") as f:
        files = {"file": ("sample.eml", f, "message/rfc822")}
        response = test_client.post("/api/v1/rules/generate_from_file", files=files)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["verdict"] == "Malicious"
    assert "reason" in json_response
    assert len(json_response["rules"]) == 2
    mock_ollama_chat.assert_called_once()

