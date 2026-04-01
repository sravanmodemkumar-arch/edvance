"""Tenant and Shard data access."""
from __future__ import annotations
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.tenancy.models.tenant import Tenant, TenantStatus, TenantPlan, _PLAN_LIMITS
from api.modules.tenancy.models.shard import Shard
from api.modules.tenancy.models.quota_event import TenantQuotaEvent, QuotaEventType


class TenantRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    # ─── Tenant lookups ────────────────────────────────────────────────────────

    async def get_by_id(self, tenant_id: int) -> Tenant | None:
        return await self._s.get(Tenant, tenant_id)

    async def get_by_uid(self, uid: str) -> Tenant | None:
        r = await self._s.execute(select(Tenant).where(Tenant.uid == uid))
        return r.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tenant | None:
        r = await self._s.execute(select(Tenant).where(Tenant.slug == slug))
        return r.scalar_one_or_none()

    async def get_by_custom_domain(self, domain: str) -> Tenant | None:
        r = await self._s.execute(select(Tenant).where(Tenant.custom_domain == domain))
        return r.scalar_one_or_none()

    async def create(self, **kwargs) -> Tenant:
        tenant = Tenant(**kwargs)
        self._s.add(tenant)
        await self._s.flush()
        return tenant

    async def update_status(self, tenant_id: int, status: TenantStatus, **extra) -> None:
        await self._s.execute(
            update(Tenant).where(Tenant.id == tenant_id).values(status=status, **extra)
        )
        await self._s.flush()

    async def update_plan(self, tenant_id: int, plan: TenantPlan) -> None:
        limits = _PLAN_LIMITS[plan]
        await self._s.execute(
            update(Tenant).where(Tenant.id == tenant_id).values(plan=plan, **limits)
        )
        await self._s.flush()

    async def increment_students(self, tenant_id: int, delta: int = 1) -> int:
        r = await self._s.execute(
            update(Tenant)
            .where(Tenant.id == tenant_id)
            .values(current_students=Tenant.current_students + delta)
            .returning(Tenant.current_students)
        )
        await self._s.flush()
        return r.scalar_one()

    async def increment_staff(self, tenant_id: int, delta: int = 1) -> int:
        r = await self._s.execute(
            update(Tenant)
            .where(Tenant.id == tenant_id)
            .values(current_staff=Tenant.current_staff + delta)
            .returning(Tenant.current_staff)
        )
        await self._s.flush()
        return r.scalar_one()

    async def add_storage_mb(self, tenant_id: int, mb: int) -> int:
        r = await self._s.execute(
            update(Tenant)
            .where(Tenant.id == tenant_id)
            .values(storage_used_mb=Tenant.storage_used_mb + mb)
            .returning(Tenant.storage_used_mb)
        )
        await self._s.flush()
        return r.scalar_one()

    # ─── Shard assignment ──────────────────────────────────────────────────────

    async def get_least_full_shard(self) -> Shard | None:
        r = await self._s.execute(
            select(Shard)
            .where(Shard.is_active.is_(True), Shard.current_tenants < Shard.max_tenants)
            .order_by(Shard.current_tenants.asc())
            .limit(1)
        )
        return r.scalar_one_or_none()

    async def increment_shard_count(self, shard_id: str) -> None:
        await self._s.execute(
            update(Shard).where(Shard.id == shard_id)
            .values(current_tenants=Shard.current_tenants + 1)
        )
        await self._s.flush()

    # ─── Quota events ──────────────────────────────────────────────────────────

    async def log_quota_event(self, tenant_id: int, event_type: QuotaEventType, **kwargs) -> None:
        self._s.add(TenantQuotaEvent(tenant_id=tenant_id, event_type=event_type, **kwargs))
        await self._s.flush()
