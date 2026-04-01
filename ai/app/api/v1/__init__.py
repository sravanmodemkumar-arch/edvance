"""ai service — API v1 router."""
from fastapi import APIRouter
from app.api.v1 import health

router = APIRouter()
router.include_router(health.router, tags=["health"])
# TODO: add feature routers as modules are built
