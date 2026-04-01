"""Visitor management — walk-in, pre-booked appointments, QR gate pass."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin


class VisitorPurpose(str, enum.Enum):
    PARENT_MEETING = "PARENT_MEETING"
    OFFICIAL = "OFFICIAL"
    DELIVERY = "DELIVERY"
    MAINTENANCE = "MAINTENANCE"
    INTERVIEW = "INTERVIEW"
    INSPECTION = "INSPECTION"
    OTHER = "OTHER"


class GatePassStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class Visitor(Base, TimestampMixin, TenantMixin):
    """One row per visit — separate record for each visit, not per person."""
    __tablename__ = "visitors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, index=True
    )
    visitor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    visitor_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    visitor_id_type: Mapped[str] = mapped_column(String(20), nullable=False, default="AADHAR")
    visitor_id_number: Mapped[str | None] = mapped_column(String(30), nullable=True)
    purpose: Mapped[VisitorPurpose] = mapped_column(
        Enum(VisitorPurpose, name="visitor_purpose_enum"), nullable=False
    )
    host_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    host_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    student_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    appointment_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    gate_pass_status: Mapped[GatePassStatus] = mapped_column(
        Enum(GatePassStatus, name="gate_pass_status_enum"),
        nullable=False, default=GatePassStatus.PENDING,
    )
    # UUID token printed/shown as QR code — gate staff scans to check in/out
    qr_token: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    expected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    checked_in_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    checked_out_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    vehicle_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
