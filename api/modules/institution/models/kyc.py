"""KYC documents — EduForge-controlled verification, not mandatory for operation."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin


class KYCDocType(str, enum.Enum):
    PAN = "PAN"
    GST = "GST"
    REG_CERT = "REG_CERT"        # Registration certificate
    AFFILIATION = "AFFILIATION"  # Board affiliation letter
    LAND_DEED = "LAND_DEED"
    NOC = "NOC"                  # No Objection Certificate
    FIRE_SAFETY = "FIRE_SAFETY"
    MINORITY_CERT = "MINORITY_CERT"
    OTHER = "OTHER"


class KYCStatus(str, enum.Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class KYCDocument(Base, TimestampMixin, TenantMixin):
    """One document per upload — an institution can upload many KYC docs."""
    __tablename__ = "institution_kyc_documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, index=True
    )
    doc_type: Mapped[KYCDocType] = mapped_column(
        Enum(KYCDocType, name="kyc_doc_type_enum"), nullable=False
    )
    document_url: Mapped[str] = mapped_column(String(512), nullable=False)
    doc_number: Mapped[str | None] = mapped_column(String(60), nullable=True)
    status: Mapped[KYCStatus] = mapped_column(
        Enum(KYCStatus, name="kyc_status_enum"),
        nullable=False, default=KYCStatus.PENDING,
    )
    # Only EduForge platform staff can approve
    reviewed_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
