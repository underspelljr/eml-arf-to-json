import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.telemetry import setup_telemetry

# Setup logging configuration
setup_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to setup and teardown the application.
    """
    logger.info("Starting up application...")
    # Setup telemetry
    setup_telemetry(app)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Include the main API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint providing basic information.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "documentation": "/docs",
    }


logger.info(
    "%s v%s started successfully", settings.APP_NAME, settings.APP_VERSION
)
