from pathlib import Path
from fastapi.testclient import TestClient

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
        SAMPLE_EML_PATH.write_text("Subject: Test EML\n\nHello World")

    with open(SAMPLE_EML_PATH, "rb") as f:
        files = {"file": ("sample.eml", f, "message/rfc822")}
        response = test_client.post("/api/v1/parse_message", files=files)

    assert response.status_code == 200
    json_response = response.json()
    assert "header" in json_response
    assert "body" in json_response
    assert json_response["header"]["subject"] == "Test EML"


def test_parse_message_file_invalid_extension(test_client: TestClient):
    """
    Test the /parse_message endpoint with a file that has an invalid extension.
    """
    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = test_client.post("/api/v1/parse_message", files=files)

    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_parse_message_file_no_file(test_client: TestClient):
    """
    Test that the endpoint returns a 422 Unprocessable Entity
    if no file is provided.
    """
    response = test_client.post("/api/v1/parse_message")
    assert response.status_code == 422  # FastAPI's validation error code
