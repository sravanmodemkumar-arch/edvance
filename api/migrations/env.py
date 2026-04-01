"""Alembic env — async SQLAlchemy, all models imported for autogenerate."""
from __future__ import annotations
import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Import Base and ALL models so Alembic can detect schema changes
from shared.db.base import Base
from api.modules.auth.models import User, UserTenant, Session, PasswordResetToken, OTP, OTPRateLimit  # noqa: F401
from api.modules.tenancy.models import Tenant, Shard, TenantQuotaEvent  # noqa: F401
from shared.db.audit import AuditLog  # noqa: F401

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Override URL from environment (12-factor)
DATABASE_URL = os.environ.get("DATABASE_URL", config.get_main_option("sqlalchemy.url", ""))
# Ensure asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema="platform",
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema="platform",
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
