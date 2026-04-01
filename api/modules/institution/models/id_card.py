"""ID card templates and issued cards — Indian format {InstCode}-{Course}-{Year}-{Seq}."""
from __future__ import annotations
import enum
from datetime import date, datetime
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from shared.shared.db.base import Base
from shared.shared.db.mixins import TimestampMixin, TenantMixin


class CardHolderType(str, enum.Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"
    VISITOR = "VISITOR"
    ALUMNI = "ALUMNI"


class IDCardTemplate(Base, TimestampMixin, TenantMixin):
    """One of 30 pre-built card designs — institution picks student + staff template."""
    __tablename__ = "id_card_templates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, index=True
    )
    template_code: Mapped[str] = mapped_column(String(30), nullable=False)  # "TPL_001"..."TPL_030"
    holder_type: Mapped[CardHolderType] = mapped_column(
        Enum(CardHolderType, name="card_holder_type_enum"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    fields_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # e.g. {"show_blood_group": true, "show_bus_route": false, "show_photo": true}
    background_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    signature_url: Mapped[str | None] = mapped_column(String(512), nullable=True)


class IDCard(Base, TimestampMixin, TenantMixin):
    """One issued card per person — unique ID number, QR code, validity period."""
    __tablename__ = "id_cards"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution_profiles.id"), nullable=False, index=True
    )
    template_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("id_card_templates.id"), nullable=True
    )
    holder_type: Mapped[CardHolderType] = mapped_column(
        Enum(CardHolderType, name="card_holder_type_enum"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    id_number: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    # Formatted as: {INST_CODE}-{COURSE}-{YEAR}-{SEQ:05d}  e.g. "DPS-X-2024-00001"
    course_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    academic_year: Mapped[str | None] = mapped_column(String(9), nullable=True)   # "2024-25"
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    qr_data: Mapped[str | None] = mapped_column(String(512), nullable=True)  # JSON-encoded payload
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoke_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    card_url: Mapped[str | None] = mapped_column(String(512), nullable=True)  # PDF/image URL
