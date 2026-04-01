"""User and UserTenant models.

Users exist at platform level; UserTenant links them to institutions.
A single user can belong to multiple tenants (e.g., teacher at 2 schools).
"""
from __future__ import annotations
import enum
from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, ForeignKey,
    Integer, String, UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.db.base import Base
from shared.db.mixins import TimestampMixin, SoftDeleteMixin


class InstitutionType(str, enum.Enum):
    SCHOOL = "SCHOOL"
    COACHING = "COACHING"
    HOSTEL = "HOSTEL"
    PLATFORM = "PLATFORM"        # B2C exam-prep users


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"


class User(Base, TimestampMixin, SoftDeleteMixin):
    """Platform-level user record. No tenant_id here — see UserTenant."""

    __tablename__ = "users"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(26), unique=True, nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(254), unique=True, nullable=True, index=True)
    mobile: Mapped[str | None] = mapped_column(String(10), unique=True, nullable=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, schema="platform"), nullable=False, default=UserStatus.ACTIVE
    )
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    locked_until: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    tenants: Mapped[list["UserTenant"]] = relationship(back_populates="user", lazy="select")


class UserTenant(Base, TimestampMixin):
    """Links a user to an institution with their roles."""

    __tablename__ = "user_tenants"
    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
        {"schema": "platform"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    institution_type: Mapped[InstitutionType] = mapped_column(
        Enum(InstitutionType, schema="platform"), nullable=False
    )
    roles: Mapped[str] = mapped_column(String(512), nullable=False)  # CSV: "TEACHER,COORDINATOR"
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped["User"] = relationship(back_populates="tenants", lazy="select")
