"""Role definitions — system templates + custom institution roles."""
from __future__ import annotations
import enum
from sqlalchemy import BigInteger, Boolean, Enum, Integer, JSON, String, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base
from shared.db.mixins import TimestampMixin, TenantMixin


class RoleGroup(str, enum.Enum):
    PLATFORM = "PLATFORM"
    GROUP = "GROUP"
    SCHOOL = "SCHOOL"
    COLLEGE = "COLLEGE"
    COACHING = "COACHING"
    EXAM_DOMAIN = "EXAM_DOMAIN"
    TSP = "TSP"
    PARENT = "PARENT"
    B2B = "B2B"
    STUDENT = "STUDENT"
    ALUMNI = "ALUMNI"


class Role(Base, TimestampMixin, TenantMixin):
    """One row per role — system roles (is_system=True) + custom institution roles.

    permissions: JSON array of "module:action:scope" strings.
    System roles use in-memory PERMISSION_MAP; DB stores for custom roles.
    """
    __tablename__ = "roles"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)         # "Class Teacher"
    code: Mapped[str] = mapped_column(String(40), nullable=False)         # "CLASS_TEACHER"
    role_group: Mapped[RoleGroup] = mapped_column(
        Enum(RoleGroup, schema="platform"), nullable=False
    )
    hierarchy_level: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permissions: Mapped[list | None] = mapped_column(JSON, nullable=True)  # custom roles only
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    approved_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RoleChangeLog(Base):
    """Immutable audit trail — every role change, assignment, removal."""
    __tablename__ = "role_change_log"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    target_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    changed_by_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)  # ASSIGNED|REMOVED|MODIFIED|EXPIRED
    role_code: Mapped[str] = mapped_column(String(40), nullable=False)
    previous_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    acknowledged_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
