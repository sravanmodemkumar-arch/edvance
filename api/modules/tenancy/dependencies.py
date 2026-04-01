"""Tenancy FastAPI dependencies.

Usage in routers:
    tenant: Tenant = Depends(get_tenant)               # resolved from state or JWT
    tenant: Tenant = Depends(require_active_tenant)    # 403 if suspended
    _: None = Depends(check_write_allowed)             # 451 if suspended
"""
from __future__ import annotations
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.modules.tenancy.models.tenant import Tenant, TenantStatus
from api.modules.tenancy.repositories.tenant_repo import TenantRepository
from shared.schemas.token_schema import TokenPayload

_WRITE_BLOCKED = {TenantStatus.SUSPENDED, TenantStatus.TERMINATED, TenantStatus.ARCHIVED}


async def get_tenant(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Tenant | None:
    """Resolve tenant from request state (middleware) or from JWT claim."""
    tenant = getattr(request.state, "tenant", None)
    if tenant:
        return tenant

    # Fallback: resolve from JWT bearer token (mobile app / API clients)
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        from shared.jwt.verify import verify_token_optional
        payload: TokenPayload | None = verify_token_optional(auth[7:])
        if payload and payload.tenant_id:
            try:
                tid = int(payload.tenant_id)
                repo = TenantRepository(db)
                return await repo.get_by_id(tid)
            except (ValueError, TypeError):
                pass
    return None


async def require_active_tenant(
    tenant: Tenant | None = Depends(get_tenant),
) -> Tenant:
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Institution not found")
    if tenant.status in _WRITE_BLOCKED:
        raise HTTPException(status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                            "Institution account is suspended or terminated")
    if tenant.status == TenantStatus.WARNING:
        pass  # allow reads + writes; warning shown via response header
    return tenant


async def check_write_allowed(tenant: Tenant = Depends(require_active_tenant)) -> None:
    """Dependency that blocks writes when tenant is suspended."""
    if tenant.status in _WRITE_BLOCKED:
        raise HTTPException(status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                            "Data entry blocked — account suspended")


async def require_module(module_name: str):
    """Factory: use as Depends(require_module('hostel'))."""
    async def _check(tenant: Tenant = Depends(require_active_tenant)) -> None:
        modules = tenant.enabled_modules or []
        if module_name not in modules:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Module '{module_name}' is not enabled for this institution",
            )
    return _check


def make_tenant_resolver(engine):
    """Build the resolver injected into TenantMiddleware at startup.

    Accepts either SQLAlchemy async engine or a callable for tests.
    """
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
    from sqlalchemy import select
    from api.modules.tenancy.models.tenant import Tenant as T

    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def resolver(slug: str) -> T | None:
        async with factory() as session:
            r = await session.execute(select(T).where(T.slug == slug))
            return r.scalar_one_or_none()

    return resolver
