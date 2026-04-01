"""TenantQuotaEvent — audit trail for quota changes and plan upgrades."""
from __future__ import annotations
import enum
from sqlalchemy import BigInteger, Enum, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base


class QuotaEventType(str, enum.Enum):
    STUDENT_ADDED = "STUDENT_ADDED"
    STUDENT_REMOVED = "STUDENT_REMOVED"
    STAFF_ADDED = "STAFF_ADDED"
    STAFF_REMOVED = "STAFF_REMOVED"
    PLAN_UPGRADED = "PLAN_UPGRADED"
    PLAN_DOWNGRADED = "PLAN_DOWNGRADED"
    SOFT_LIMIT_WARNING = "SOFT_LIMIT_WARNING"   # 90% reached
    HARD_LIMIT_REACHED = "HARD_LIMIT_REACHED"
    STORAGE_WARNING = "STORAGE_WARNING"          # 80% storage
    STORAGE_FULL = "STORAGE_FULL"


class TenantQuotaEvent(Base):
    """Immutable audit trail — never update or delete."""
    __tablename__ = "tenant_quota_events"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("platform.tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    event_type: Mapped[QuotaEventType] = mapped_column(
        Enum(QuotaEventType, schema="platform"), nullable=False
    )
    old_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    new_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actor_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
