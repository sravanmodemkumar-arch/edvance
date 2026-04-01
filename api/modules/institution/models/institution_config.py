"""Institution academic config — one-to-one with InstitutionProfile."""
from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin


class InstitutionConfig(Base, TimestampMixin, TenantMixin):
    """Academic config, infrastructure flags, compliance, and feature toggles."""
    __tablename__ = "institution_configs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, unique=True, index=True
    )
    # Academic
    academic_year_start_month: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    grading_system: Mapped[str] = mapped_column(String(20), nullable=False, default="MARKS")
    # MARKS | GRADE | CGPA | PERCENTAGE
    attendance_threshold_pct: Mapped[int] = mapped_column(Integer, nullable=False, default=75)
    working_days_per_week: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    periods_per_day: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    period_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    # School-specific
    num_classes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sections_per_class: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_house_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # College-specific
    has_semester_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Coaching-specific
    is_batch_based: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Infrastructure
    has_hostel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_transport: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_library: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_canteen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_smart_classes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Features
    fee_lock_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    enabled_modules: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    # Branding — 20 themes × 10 layouts = 200 combinations
    theme_code: Mapped[str] = mapped_column(String(30), nullable=False, default="DEFAULT")
    layout_code: Mapped[str] = mapped_column(String(30), nullable=False, default="CLASSIC")
    # Compliance
    pocso_officer_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    pocso_officer_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    dpdpa_contact_email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    # KYC (EduForge-controlled, not mandatory)
    is_kyc_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Alumni — no login, auto-inactive after graduation
    alumni_auto_inactive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # ID card number format — uses {INST_CODE}, {COURSE}, {YEAR}, {SEQ:05d}
    id_card_format: Mapped[str] = mapped_column(
        String(80), nullable=False, default="{INST_CODE}-{COURSE}-{YEAR}-{SEQ:05d}"
    )
    # Bulk operations require two-level auth (Principal + VP/Admin)
    bulk_ops_two_level_auth: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
