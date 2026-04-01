"""Shard registry — one row per PostgreSQL shard node."""
from __future__ import annotations
from sqlalchemy import BigInteger, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from shared.db.base import Base
from shared.db.mixins import TimestampMixin


class Shard(Base, TimestampMixin):
    """Each shard is an independent PostgreSQL cluster (or Neon project).

    Phase 1: single shard — shard-001 pointing to Neon.
    Phase 2+: multiple shards assigned by student-count tier.
    """
    __tablename__ = "shards"
    __table_args__ = {"schema": "platform"}

    id: Mapped[str] = mapped_column(String(32), primary_key=True)  # "shard-001"
    db_url_encrypted: Mapped[str] = mapped_column(String(512), nullable=False)
    region: Mapped[str] = mapped_column(String(32), nullable=False, default="ap-south-1")
    max_tenants: Mapped[int] = mapped_column(Integer, nullable=False, default=500)
    current_tenants: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
