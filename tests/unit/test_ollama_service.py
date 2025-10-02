import pytest
from unittest.mock import AsyncMock, patch
from app.services.ollama_service import generate_rules_for_eml
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_generate_rules_for_eml_success():
    """
    Test successful rule generation from EML data using a mocked Ollama client.
    """
    mock_ollama_client = AsyncMock()
    mock_ollama_client.chat.return_value = {
        "message": {
            "content": '{"verdict": "Benign", "category": "Test Category", "reason": "Mocked Ollama response", "rules": []}'
        }
    }

    with patch('app.services.ollama_service.ollama.AsyncClient', return_value=mock_ollama_client):
        parsed_data = {"header": {"subject": "Test"}, "body": []}
        result = await generate_rules_for_eml(parsed_data)

        assert result == {"verdict": "Benign", "category": "Test Category", "reason": "Mocked Ollama response", "rules": []}
        mock_ollama_client.chat.assert_called_once()

@pytest.mark.asyncio
async def test_generate_rules_for_eml_ollama_error():
    """
    Test error handling when Ollama communication fails.
    """
    mock_ollama_client = AsyncMock()
    mock_ollama_client.chat.side_effect = Exception("Ollama connection error")

    with patch('app.services.ollama_service.ollama.AsyncClient', return_value=mock_ollama_client):
        parsed_data = {"header": {"subject": "Test"}, "body": []}
        with pytest.raises(HTTPException) as exc_info:
            await generate_rules_for_eml(parsed_data)

        assert exc_info.value.status_code == 503
        assert "Could not communicate with the analysis service" in exc_info.value.detail
        mock_ollama_client.chat.assert_called_once()

@pytest.mark.asyncio
async def test_generate_rules_for_eml_json_decode_error():
    """
    Test error handling when Ollama returns invalid JSON.
    """
    mock_ollama_client = AsyncMock()
    mock_ollama_client.chat.return_value = {
        "message": {
            "content": "this is not valid json"
        }
    }

    with patch('app.services.ollama_service.ollama.AsyncClient', return_value=mock_ollama_client):
        parsed_data = {"header": {"subject": "Test"}, "body": []}
        with pytest.raises(HTTPException) as exc_info:
            await generate_rules_for_eml(parsed_data)

        assert exc_info.value.status_code == 500
        assert "Failed to parse analysis from the AI model" in exc_info.value.detail
        mock_ollama_client.chat.assert_called_once()
