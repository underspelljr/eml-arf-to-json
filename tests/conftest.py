import sys
import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.main import app


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    Creates a FastAPI TestClient for integration tests.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
async def async_test_client() -> AsyncClient:
    """
    Creates an asynchronous test client.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
