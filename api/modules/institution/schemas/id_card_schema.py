"""ID card schemas — templates and issued cards."""
from __future__ import annotations
from datetime import date, datetime
from pydantic import BaseModel, Field
from api.modules.institution.models.id_card import CardHolderType


class IDCardTemplateCreate(BaseModel):
    template_code: str = Field(..., pattern=r"^TPL_\d{3}$", description="e.g. TPL_001")
    holder_type: CardHolderType
    fields_config: dict | None = None
    background_url: str | None = None
    signature_url: str | None = None


class IDCardTemplateOut(BaseModel):
    id: int
    institution_id: int
    template_code: str
    holder_type: CardHolderType
    is_active: bool
    fields_config: dict | None
    background_url: str | None

    model_config = {"from_attributes": True}


class IDCardIssueRequest(BaseModel):
    """Issue an ID card to a user — system generates the ID number."""
    user_id: int
    holder_type: CardHolderType
    template_id: int | None = None
    course_code: str | None = Field(None, max_length=20)
    academic_year: str | None = Field(None, pattern=r"^\d{4}-\d{2}$")  # "2024-25"
    valid_from: date
    valid_until: date


class IDCardOut(BaseModel):
    id: int
    institution_id: int
    user_id: int
    id_number: str       # e.g. "DPS-X-2024-00001"
    holder_type: CardHolderType
    course_code: str | None
    academic_year: str | None
    valid_from: date
    valid_until: date
    qr_data: str | None
    is_active: bool
    revoked_at: datetime | None
    card_url: str | None

    model_config = {"from_attributes": True}


class IDCardRevokeRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=255)
