"""PostgreSQL Row-Level Security context helpers.

Sets app.tenant_id session variable so RLS policies auto-filter all queries.
RLS policies on tenant tables:
    USING (tenant_id = current_setting('app.tenant_id', TRUE)::BIGINT)

Super-admin: connect with a DB user that has BYPASSRLS privilege, or
             pass tenant_id=None to run without tenant filter (audit queries).
"""
from __future__ import annotations
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def set_tenant_context(session: AsyncSession, tenant_id: int) -> None:
    """Call once per request before any tenant-scoped query."""
    await session.execute(text(f"SET LOCAL app.tenant_id = {int(tenant_id)}"))


async def clear_tenant_context(session: AsyncSession) -> None:
    """Clears the setting (e.g. for super-admin cross-tenant queries)."""
    await session.execute(text("SET LOCAL app.tenant_id = ''"))


def rls_policy_sql(table: str, schema: str = "public") -> list[str]:
    """Return SQL statements to enable RLS on a table.

    Call from migrations for every tenant-scoped table.
    """
    return [
        f'ALTER TABLE "{schema}"."{table}" ENABLE ROW LEVEL SECURITY',
        f'ALTER TABLE "{schema}"."{table}" FORCE ROW LEVEL SECURITY',
        f"""CREATE POLICY tenant_isolation ON "{schema}"."{table}"
            USING (tenant_id = current_setting('app.tenant_id', TRUE)::BIGINT)
            WITH CHECK (tenant_id = current_setting('app.tenant_id', TRUE)::BIGINT)""",
    ]
