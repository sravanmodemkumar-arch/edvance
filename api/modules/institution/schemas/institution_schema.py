"""Institution onboarding and profile schemas."""
from __future__ import annotations
import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from api.modules.institution.models.institution import InstitutionType, InstitutionStatus

_PIN_RE = re.compile(r"^\d{6}$")
_PHONE_RE = re.compile(r"^[6-9]\d{9}$")
_PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
_UDISE_RE = re.compile(r"^\d{11}$")


class OnboardingRequest(BaseModel):
    """Full 91-point onboarding payload — collected during institution signup."""
    institution_type: InstitutionType
    legal_name: str = Field(..., min_length=3, max_length=300)
    display_name: str = Field(..., min_length=2, max_length=120)
    short_code: str = Field(..., min_length=2, max_length=6, description="2-6 uppercase chars for ID cards")
    # India identity
    registration_number: str | None = None
    registration_authority: str | None = None
    affiliation_board: str | None = None
    affiliation_number: str | None = None
    establishment_year: int | None = Field(None, ge=1800, le=2100)
    udise_code: str | None = None
    trust_society_name: str | None = None
    trust_reg_number: str | None = None
    gst_number: str | None = None
    pan_number: str | None = None
    # Address
    address_line1: str = Field(..., min_length=5, max_length=255)
    address_line2: str | None = None
    city: str = Field(..., min_length=2, max_length=80)
    district: str | None = None
    state: str = Field(..., min_length=2, max_length=80)
    pin_code: str
    latitude: float | None = None
    longitude: float | None = None
    # Contact
    phone: str
    alternate_phone: str | None = None
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    website: str | None = None
    # Leadership
    principal_name: str | None = None
    principal_phone: str | None = None
    principal_email: str | None = None
    correspondent_name: str | None = None
    correspondent_phone: str | None = None

    @field_validator("short_code")
    @classmethod
    def validate_short_code(cls, v: str) -> str:
        if not v.isupper() or not v.isalpha():
            raise ValueError("short_code must be uppercase letters only e.g. DPS, KV")
        return v

    @field_validator("pin_code")
    @classmethod
    def validate_pin(cls, v: str) -> str:
        if not _PIN_RE.match(v):
            raise ValueError("pin_code must be exactly 6 digits")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not _PHONE_RE.match(v):
            raise ValueError("Phone must be 10 digits starting 6-9")
        return v

    @field_validator("udise_code")
    @classmethod
    def validate_udise(cls, v: str | None) -> str | None:
        if v and not _UDISE_RE.match(v):
            raise ValueError("UDISE code must be exactly 11 digits")
        return v

    @field_validator("pan_number")
    @classmethod
    def validate_pan(cls, v: str | None) -> str | None:
        if v and not _PAN_RE.match(v):
            raise ValueError("Invalid PAN format (e.g. ABCDE1234F)")
        return v


class InstitutionProfileOut(BaseModel):
    id: int
    tenant_id: int
    institution_type: InstitutionType
    legal_name: str
    display_name: str
    short_code: str
    city: str
    state: str
    phone: str
    email: str
    status: InstitutionStatus
    is_trial: bool
    trial_ends_at: datetime | None
    provisioned_at: datetime | None
    logo_url: str | None

    model_config = {"from_attributes": True}
