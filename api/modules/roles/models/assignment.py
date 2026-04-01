"""RoleAssignment and RoleDelegation — who has which role, for how long."""
from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base
from shared.db.mixins import TimestampMixin


class RoleAssignment(Base, TimestampMixin):
    """Links a UserTenant to one Role. Temporal: null ends_at = permanent.

    scope_context: JSON — which class/dept/batch the role applies to.
    Example: {"class_id": 12, "section": "A"} for a Class Teacher assignment.
    """
    __tablename__ = "role_assignments"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    role_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("platform.roles.id"), nullable=False, index=True
    )
    role_code: Mapped[str] = mapped_column(String(40), nullable=False)   # denormalized for speed
    starts_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    assigned_by_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    scope_context: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Acknowledged by assigned user within 48 hrs
    acknowledged_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RoleDelegation(Base, TimestampMixin):
    """Time-bound authority delegation — delegator gives subset of authority to delegate.

    All actions under delegation logged with both delegator_id and delegate_id.
    """
    __tablename__ = "role_delegations"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    delegator_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    delegate_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    role_code: Mapped[str] = mapped_column(String(40), nullable=False)
    permissions: Mapped[list] = mapped_column(JSON, nullable=False)   # subset of delegator's perms
    starts_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
