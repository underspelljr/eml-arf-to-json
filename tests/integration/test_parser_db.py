import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.api.v1.endpoints.parser import get_db
from app.models.email import Base, ParsedEmail, RawEmail

# Use a test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture(name="client")
def client_fixture(db_session: TestingSessionLocal, mocker):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Mock the ollama.chat function to prevent actual Ollama calls during testing
    mock_ollama_client = mocker.patch(
        "app.services.ollama_service.ollama.AsyncClient"
    )
    mock_ollama_client.return_value.chat.return_value = AsyncMock(return_value={
        "message": {
            "content": '{"verdict": "Benign", "category": "Test Category", "reason": "Mocked Ollama response", "rules": []}'
        }
    }).return_value

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_parse_eml_and_save_to_db(client: TestClient):
    # Create a dummy EML file content
    eml_content = (
        b"From: test@example.com\n"
        b"To: recipient@example.com\n"
        b"Subject: Test EML File\n"
        b"Date: Thu, 02 Oct 2025 10:00:00 +0000\n"
        b"X-Sender-IP: 192.168.1.1\n"
        b"\n"
        b"This is the body of the test EML file."
    )

    files = {"file": ("test.eml", eml_content, "message/rfc822")}
    response = client.post("/api/v1/rules/generate_from_file", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Benign"
    assert data["category"] == "Test Category"

    # Verify data in the database
    db = TestingSessionLocal()
    parsed_email = db.query(ParsedEmail).filter(ParsedEmail.subject == "Test EML File").first()
    assert parsed_email is not None
    assert parsed_email.from_address == "test@example.com"
    assert parsed_email.to_address == "recipient@example.com"
    assert parsed_email.sender_ip == "192.168.1.1"
    assert parsed_email.ollama_evaluation == json.dumps({"verdict": "Benign", "category": "Test Category", "reason": "Mocked Ollama response", "rules": []})

    raw_email = db.query(RawEmail).filter(RawEmail.parsed_email_id == parsed_email.id).first()
    assert raw_email is not None
    assert raw_email.raw_content == eml_content.decode('utf-8').replace('\x00', '')


def test_parse_arf_and_save_to_db(client: TestClient):
    # Create a dummy ARF file content
    arf_content = (
        b"From: arf_sender@example.com\n"
        b"To: arf_recipient@example.com\n"
        b"Subject: Test ARF File\n"
        b"Date: Thu, 02 Oct 2025 11:00:00 +0000\n"
        b"X-Sender-IP: 10.0.0.1\n"
        b"\n"
        b"This is the body of the test ARF file."
    )

    files = {"file": ("test.arf", arf_content, "message/rfc822")}
    response = client.post("/api/v1/rules/generate_from_file", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Benign"
    assert data["category"] == "Test Category"

    # Verify data in the database
    db = TestingSessionLocal()
    parsed_email = db.query(ParsedEmail).filter(ParsedEmail.subject == "Test ARF File").first()
    assert parsed_email is not None
    assert parsed_email.from_address == "arf_sender@example.com"
    assert parsed_email.to_address == "arf_recipient@example.com"
    assert parsed_email.sender_ip == "10.0.0.1"
    assert parsed_email.ollama_evaluation == json.dumps({"verdict": "Benign", "category": "Test Category", "reason": "Mocked Ollama response", "rules": []})

    raw_email = db.query(RawEmail).filter(RawEmail.parsed_email_id == parsed_email.id).first()
    assert raw_email is not None
    assert raw_email.raw_content == arf_content.decode('utf-8').replace('\x00', '')
