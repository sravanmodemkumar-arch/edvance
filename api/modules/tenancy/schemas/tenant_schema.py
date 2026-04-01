"""Tenant request/response schemas."""
from __future__ import annotations
import re
from pydantic import BaseModel, Field, field_validator
from api.modules.tenancy.models.tenant import TenantType, TenantPlan, TenantStatus, InstitutionBoard

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,78}[a-z0-9]$")
_HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., description="dps-delhi — used in subdomain")
    tenant_type: TenantType
    plan: TenantPlan = TenantPlan.STARTER
    board: InstitutionBoard = InstitutionBoard.NA
    academic_year_start_month: int = Field(default=6, ge=1, le=12)
    admin_name: str | None = None
    admin_email: str | None = None
    admin_mobile: str | None = None
    udise_code: str | None = Field(None, min_length=11, max_length=11)
    gst_number: str | None = Field(None, min_length=15, max_length=15)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not _SLUG_RE.match(v):
            raise ValueError("Slug must be lowercase letters, digits, hyphens (3-80 chars)")
        return v.lower()


class TenantPublic(BaseModel):
    """Returned to unauthenticated requests — login page loads this."""
    uid: str
    name: str
    slug: str
    logo_url: str | None
    primary_color: str
    secondary_color: str
    font_family: str
    status: TenantStatus
    homepage_layout: dict | None
    enabled_modules: list | None
    academic_year_start_month: int
    whatsapp_enabled: bool

    model_config = {"from_attributes": True}


class TenantAdmin(TenantPublic):
    """Full detail — platform admin only."""
    id: int
    tenant_type: TenantType
    shard_id: str
    plan: TenantPlan
    max_students: int
    max_staff: int
    storage_gb: int
    current_students: int
    current_staff: int
    storage_used_mb: int
    custom_domain: str | None
    board: InstitutionBoard
    udise_code: str | None
    gst_number: str | None
    admin_name: str | None
    admin_email: str | None
    admin_mobile: str | None

    model_config = {"from_attributes": True}


class BrandingUpdate(BaseModel):
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    font_family: str | None = None

    @field_validator("primary_color", "secondary_color")
    @classmethod
    def validate_hex(cls, v: str | None) -> str | None:
        if v and not _HEX_RE.match(v):
            raise ValueError("Must be a valid hex color (#RRGGBB)")
        return v


class HomepageLayoutUpdate(BaseModel):
    sections: list[dict] = Field(..., min_length=1)


class PlanUpgrade(BaseModel):
    plan: TenantPlan


class ModuleToggle(BaseModel):
    module: str = Field(..., min_length=2, max_length=64)
    enabled: bool


class TenantStatusUpdate(BaseModel):
    status: TenantStatus
