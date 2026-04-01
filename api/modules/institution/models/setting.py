"""Institution settings — typed key-value store with optional approval workflow."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin


class SettingCategory(str, enum.Enum):
    ACADEMIC = "ACADEMIC"
    COMMUNICATION = "COMMUNICATION"
    FINANCE = "FINANCE"
    SECURITY = "SECURITY"
    ATTENDANCE = "ATTENDANCE"
    EXAM = "EXAM"
    PORTAL = "PORTAL"
    COMPLIANCE = "COMPLIANCE"


class InstitutionSetting(Base, TimestampMixin, TenantMixin):
    """Key-value config — sensitive keys require approval before activation."""
    __tablename__ = "institution_settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, index=True
    )
    category: Mapped[SettingCategory] = mapped_column(
        Enum(SettingCategory, name="setting_category_enum"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(80), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Sensitive keys (e.g. exam_policy, fee_lock_trigger) need approval
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_pending_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    pending_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    changed_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
