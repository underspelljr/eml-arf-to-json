from fastapi import APIRouter

from app.api.v1.endpoints import parser, status, rules

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(parser.router, prefix="/parser", tags=["Parser"])
api_router.include_router(rules.router, prefix="/rules", tags=["Rules"])

