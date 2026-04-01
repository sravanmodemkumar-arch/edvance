"""Institution profile — core identity, address, contact, status."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin, SoftDeleteMixin


class InstitutionType(str, enum.Enum):
    PRE_PRIMARY = "PRE_PRIMARY"
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    HIGHER_SECONDARY = "HIGHER_SECONDARY"
    INTEGRATED = "INTEGRATED"        # K-12 combined
    DEGREE_COLLEGE = "DEGREE_COLLEGE"
    ENGINEERING = "ENGINEERING"
    MEDICAL = "MEDICAL"
    COACHING = "COACHING"
    ITI = "ITI"
    POLYTECHNIC = "POLYTECHNIC"
    UNIVERSITY = "UNIVERSITY"
    INTERNATIONAL = "INTERNATIONAL"
    OPEN_SCHOOL = "OPEN_SCHOOL"
    SPECIAL_NEEDS = "SPECIAL_NEEDS"
    GROUP = "GROUP"                  # multi-campus group entity


class InstitutionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class InstitutionProfile(Base, TimestampMixin, TenantMixin, SoftDeleteMixin):
    """One row per institution — rich detail beyond the Tenant registry."""
    __tablename__ = "institution_profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_type: Mapped[InstitutionType] = mapped_column(
        Enum(InstitutionType, name="institution_type_enum"), nullable=False
    )
    legal_name: Mapped[str] = mapped_column(String(300), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    short_code: Mapped[str] = mapped_column(String(6), nullable=False)  # for ID card prefix e.g. "DPS"
    registration_number: Mapped[str | None] = mapped_column(String(60), nullable=True)
    registration_authority: Mapped[str | None] = mapped_column(String(120), nullable=True)
    affiliation_board: Mapped[str | None] = mapped_column(String(20), nullable=True)
    affiliation_number: Mapped[str | None] = mapped_column(String(40), nullable=True)
    establishment_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    udise_code: Mapped[str | None] = mapped_column(String(11), nullable=True, index=True)
    trust_society_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    trust_reg_number: Mapped[str | None] = mapped_column(String(60), nullable=True)
    gst_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    pan_number: Mapped[str | None] = mapped_column(String(10), nullable=True)
    # Address
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    district: Mapped[str | None] = mapped_column(String(80), nullable=True)
    state: Mapped[str] = mapped_column(String(80), nullable=False)
    pin_code: Mapped[str] = mapped_column(String(6), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    # Contact
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    alternate_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    website: Mapped[str | None] = mapped_column(String(253), nullable=True)
    # Leadership
    principal_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    principal_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    principal_email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    correspondent_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    correspondent_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    # Media
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Status
    status: Mapped[InstitutionStatus] = mapped_column(
        Enum(InstitutionStatus, name="institution_status_enum"),
        nullable=False, default=InstitutionStatus.DRAFT,
    )
    is_trial: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    provisioned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
