"""OTP and OTPRateLimit models.

OTPs are NOT used for login. They gate:
- Forgot password, account delete, phone/email change
- Payment > ₹10K, DSAR request, institution deactivation
"""
from __future__ import annotations
import enum
from sqlalchemy import BigInteger, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base


class OTPPurpose(str, enum.Enum):
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    ACCOUNT_DELETE = "ACCOUNT_DELETE"
    CHANGE_PHONE = "CHANGE_PHONE"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    HIGH_VALUE_PAYMENT = "HIGH_VALUE_PAYMENT"
    DSAR = "DSAR"
    DEACTIVATE_INSTITUTION = "DEACTIVATE_INSTITUTION"


class OTP(Base):
    """One active OTP per (user, purpose) at a time. Old ones are replaced."""

    __tablename__ = "otps"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    purpose: Mapped[OTPPurpose] = mapped_column(
        Enum(OTPPurpose, schema="platform"), nullable=False
    )
    otp_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    verified: Mapped[bool] = mapped_column(Integer, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class OTPRateLimit(Base):
    """Tracks OTP send counts per (mobile/email) per purpose per day."""

    __tablename__ = "otp_rate_limits"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    identifier: Mapped[str] = mapped_column(String(254), nullable=False, index=True)
    purpose: Mapped[OTPPurpose] = mapped_column(
        Enum(OTPPurpose, schema="platform"), nullable=False
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    window_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
