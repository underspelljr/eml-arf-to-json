import logging

from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.status import AppStatus

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/app_status",
    response_model=AppStatus,
    status_code=status.HTTP_200_OK,
    summary="Get Application Status",
    description="Provides the current status, name, and version of the application.",
)
async def get_app_status():
    """
    Endpoint to verify application health.
    """
    logger.info("Health check endpoint was called.")
    return {
        "status": "ok",
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
