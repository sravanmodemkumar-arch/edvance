"""Tenant model — central registry of all institutions."""
from __future__ import annotations
import enum
from sqlalchemy import (
    BigInteger, Boolean, Enum, ForeignKey, Integer,
    JSON, Numeric, String, Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base
from shared.db.mixins import TimestampMixin, SoftDeleteMixin


class TenantType(str, enum.Enum):
    SCHOOL = "SCHOOL"
    COLLEGE = "COLLEGE"
    COACHING = "COACHING"
    GROUP = "GROUP"           # multi-campus group


class TenantStatus(str, enum.Enum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    WARNING = "WARNING"       # payment 7 days overdue
    SUSPENDED = "SUSPENDED"   # payment 30 days overdue — read-only
    TERMINATED = "TERMINATED"
    ARCHIVED = "ARCHIVED"     # cold storage


class TenantPlan(str, enum.Enum):
    STARTER = "STARTER"       # ≤ 500 students
    GROWTH = "GROWTH"         # ≤ 5,000 students
    SCALE = "SCALE"           # ≤ 50,000 students
    ENTERPRISE = "ENTERPRISE" # unlimited


class InstitutionBoard(str, enum.Enum):
    CBSE = "CBSE"
    ICSE = "ICSE"
    STATE = "STATE"
    IB = "IB"
    IGCSE = "IGCSE"
    NA = "NA"                 # coaching / college / not applicable


_PLAN_LIMITS: dict[TenantPlan, dict] = {
    TenantPlan.STARTER:    {"max_students": 500,    "max_staff": 50,    "storage_gb": 5},
    TenantPlan.GROWTH:     {"max_students": 5_000,  "max_staff": 500,   "storage_gb": 50},
    TenantPlan.SCALE:      {"max_students": 50_000, "max_staff": 5_000, "storage_gb": 500},
    TenantPlan.ENTERPRISE: {"max_students": 999_999, "max_staff": 99_999, "storage_gb": 10_000},
}


class Tenant(Base, TimestampMixin, SoftDeleteMixin):
    """One row per institution in the platform central registry."""
    __tablename__ = "tenants"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(26), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    tenant_type: Mapped[TenantType] = mapped_column(
        Enum(TenantType, schema="platform"), nullable=False
    )
    shard_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("platform.shards.id"), nullable=False
    )
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus, schema="platform"), nullable=False, default=TenantStatus.PROVISIONING
    )
    plan: Mapped[TenantPlan] = mapped_column(
        Enum(TenantPlan, schema="platform"), nullable=False, default=TenantPlan.STARTER
    )
    max_students: Mapped[int] = mapped_column(Integer, nullable=False, default=500)
    max_staff: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    storage_gb: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    current_students: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    current_staff: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    storage_used_mb: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    # Routing
    custom_domain: Mapped[str | None] = mapped_column(String(253), nullable=True, unique=True)

    # Branding
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(7), nullable=False, default="#1B4F72")
    secondary_color: Mapped[str] = mapped_column(String(7), nullable=False, default="#2E86C1")
    font_family: Mapped[str] = mapped_column(String(64), nullable=False, default="Inter")
    homepage_layout: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # India-specific
    board: Mapped[InstitutionBoard] = mapped_column(
        Enum(InstitutionBoard, schema="platform"), nullable=False, default=InstitutionBoard.NA
    )
    udise_code: Mapped[str | None] = mapped_column(String(11), nullable=True)  # 11-digit govt ID
    gst_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    academic_year_start_month: Mapped[int] = mapped_column(Integer, nullable=False, default=6)

    # Modules & features (EduForge controlled)
    enabled_modules: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    whatsapp_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    whatsapp_wallet_paise: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    # Contact
    admin_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    admin_email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    admin_mobile: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Lifecycle timestamps
    suspended_at: Mapped[str | None] = mapped_column(String(30), nullable=True)
    terminated_at: Mapped[str | None] = mapped_column(String(30), nullable=True)
