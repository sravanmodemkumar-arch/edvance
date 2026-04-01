"""Login, register, token schemas."""
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field, field_validator
from shared.utils.phone import is_valid_mobile


class LoginRequest(BaseModel):
    identifier: str = Field(..., description="Email or 10-digit mobile number")
    password: str = Field(..., min_length=8)
    tenant_slug: str = Field(..., description="Institution slug e.g. 'dav-rohini'")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900
    user_id: str
    full_name: str
    roles: list[str]


class RefreshRequest(BaseModel):
    """Body unused — refresh token comes from HttpOnly cookie."""
    pass


class LogoutRequest(BaseModel):
    all_devices: bool = False


class RegisterRequest(BaseModel):
    """B2C self-registration — only for exam-prep domain."""
    full_name: str = Field(..., min_length=2, max_length=120)
    mobile: str
    email: EmailStr | None = None
    password: str = Field(..., min_length=8)
    exam_domain: str = Field(..., description="SSC | RRB | UPSC | BANKING | NEET | JEE")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        if not is_valid_mobile(v):
            raise ValueError("Invalid Indian mobile number")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        errors = []
        if not any(c.isupper() for c in v):
            errors.append("uppercase letter")
        if not any(c.islower() for c in v):
            errors.append("lowercase letter")
        if not any(c.isdigit() for c in v):
            errors.append("digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in v):
            errors.append("special character")
        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}")
        return v
