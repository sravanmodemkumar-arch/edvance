"""AuditLog — DPDPA + POCSO compliance.

All PII access must be logged. Use make_audit_entry() to create entries;
caller is responsible for adding to session (sync or async).
"""
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Integer, JSON, Text, func
from shared.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "platform"}

    id: Mapped[int] = mapped_column(primary_key=True)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(10), nullable=False)  # CREATE READ UPDATE DELETE
    actor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_fields: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


def make_audit_entry(
    table_name: str,
    record_id: int,
    action: str,
    actor_id: int | None = None,
    tenant_id: int | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    changed_fields: dict[str, Any] | None = None,
) -> AuditLog:
    """Build an AuditLog instance. Caller adds to session."""
    return AuditLog(
        table_name=table_name,
        record_id=record_id,
        action=action,
        actor_id=actor_id,
        tenant_id=tenant_id,
        ip_address=ip_address,
        user_agent=user_agent,
        changed_fields=changed_fields,
    )
