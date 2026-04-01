"""Schemas for OTP, password, and account-ops flows."""
from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from api.modules.auth.models.otp import OTPPurpose
from shared.utils.phone import is_valid_mobile


class SendOTPRequest(BaseModel):
    identifier: str = Field(..., description="Mobile or email")
    purpose: OTPPurpose


class VerifyOTPRequest(BaseModel):
    identifier: str
    purpose: OTPPurpose
    otp: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    identifier: str = Field(..., description="Email or mobile")
    tenant_slug: str


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_strength(cls, v: str) -> str:
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


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class ChangePhoneRequest(BaseModel):
    new_mobile: str
    otp: str = Field(..., min_length=6, max_length=6)

    @field_validator("new_mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        if not is_valid_mobile(v):
            raise ValueError("Invalid Indian mobile number")
        return v
