from fastapi import APIRouter

from app.api.v1.endpoints import parser, status

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(status.router, tags=["Status"])
api_router.include_router(parser.router, tags=["Parser"])
