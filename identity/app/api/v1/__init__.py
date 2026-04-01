"""API v1 router — aggregates all identity endpoints."""
from fastapi import APIRouter
from app.api.v1 import auth_login, auth_otp, auth_refresh, users, health

router = APIRouter()
router.include_router(auth_login.router, prefix="/auth", tags=["auth"])
router.include_router(auth_otp.router, prefix="/auth", tags=["auth"])
router.include_router(auth_refresh.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(health.router, tags=["health"])
