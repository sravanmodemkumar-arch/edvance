"""Auth request/response schemas."""
from .auth_schema import (
    LoginRequest, LoginResponse,
    RefreshRequest, LogoutRequest,
    RegisterRequest,
)
from .ops_schema import (
    SendOTPRequest, VerifyOTPRequest,
    ForgotPasswordRequest, ResetPasswordRequest,
    ChangePasswordRequest, ChangePhoneRequest,
)

__all__ = [
    "LoginRequest", "LoginResponse",
    "RefreshRequest", "LogoutRequest",
    "RegisterRequest",
    "SendOTPRequest", "VerifyOTPRequest",
    "ForgotPasswordRequest", "ResetPasswordRequest",
    "ChangePasswordRequest", "ChangePhoneRequest",
]
