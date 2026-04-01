"""Async SQLAlchemy engine + session factory.

Phase 1 (VPS): connects to Neon PostgreSQL (built-in pooling).
Phase 2+ (Lambda): RDS Proxy sits in front — DO NOT use pool_size > 5.
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from api.core.config import get_settings


def _build_url(raw: str) -> str:
    """Convert sync postgresql:// to async postgresql+asyncpg://."""
    return (
        raw.replace("postgresql://", "postgresql+asyncpg://")
           .replace("postgres://", "postgresql+asyncpg://")
    )


def _make_engine():
    s = get_settings()
    # Lambda: keep pool small — RDS Proxy handles connection pooling
    pool_size = 2 if s.infra_provider in ("hybrid", "aws") else s.database_pool_size
    return create_async_engine(
        _build_url(s.database_url),
        pool_size=pool_size,
        max_overflow=s.database_max_overflow,
        pool_pre_ping=True,
        echo=s.debug and s.app_env == "dev",
    )


_engine = _make_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """FastAPI dependency — yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
