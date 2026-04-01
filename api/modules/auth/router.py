"""Auth module — aggregates login, OTP, and profile routers."""
from fastapi import APIRouter
from api.modules.auth.routers.login_router import router as login_router
from api.modules.auth.routers.otp_router import router as otp_router
from api.modules.auth.routers.profile_router import router as profile_router

router = APIRouter()
router.include_router(login_router)
router.include_router(otp_router)
router.include_router(profile_router)
