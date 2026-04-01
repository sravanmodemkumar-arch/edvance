"""Auth routers."""
from .login_router import router as login_router
from .otp_router import router as otp_router
from .profile_router import router as profile_router

__all__ = ["login_router", "otp_router", "profile_router"]
