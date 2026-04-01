"""Tenant lifecycle — provisioning, status transitions, plan upgrades."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.tenancy.models.tenant import (
    Tenant, TenantPlan, TenantStatus, TenantType, InstitutionBoard, _PLAN_LIMITS,
)
from api.modules.tenancy.repositories.tenant_repo import TenantRepository

_UID_PREFIX = "tnt"


class TenantService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TenantRepository(session)

    async def provision(
        self,
        *,
        name: str,
        slug: str,
        tenant_type: TenantType,
        plan: TenantPlan = TenantPlan.STARTER,
        board: InstitutionBoard = InstitutionBoard.NA,
        academic_year_start_month: int = 6,
        admin_name: str | None = None,
        admin_email: str | None = None,
        admin_mobile: str | None = None,
        udise_code: str | None = None,
        gst_number: str | None = None,
    ) -> Tenant:
        # Validate slug uniqueness
        existing = await self._repo.get_by_slug(slug)
        if existing:
            raise HTTPException(status.HTTP_409_CONFLICT, f"Slug '{slug}' already taken")

        # Assign least-full shard
        shard = await self._repo.get_least_full_shard()
        if not shard:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "No available shard")

        limits = _PLAN_LIMITS[plan]
        uid = f"{_UID_PREFIX}_{uuid.uuid4().hex[:10]}"
        tenant = await self._repo.create(
            uid=uid,
            name=name,
            slug=slug,
            tenant_type=tenant_type,
            shard_id=shard.id,
            status=TenantStatus.PROVISIONING,
            plan=plan,
            board=board,
            academic_year_start_month=academic_year_start_month,
            admin_name=admin_name,
            admin_email=admin_email,
            admin_mobile=admin_mobile,
            udise_code=udise_code,
            gst_number=gst_number,
            enabled_modules=[],
            **limits,
        )
        await self._repo.increment_shard_count(shard.id)
        return tenant

    async def activate(self, tenant_id: int) -> None:
        await self._repo.update_status(tenant_id, TenantStatus.ACTIVE)

    async def warn(self, tenant_id: int) -> None:
        await self._repo.update_status(tenant_id, TenantStatus.WARNING)

    async def suspend(self, tenant_id: int) -> None:
        await self._repo.update_status(
            tenant_id, TenantStatus.SUSPENDED,
            suspended_at=datetime.now(timezone.utc).isoformat(),
        )

    async def terminate(self, tenant_id: int) -> None:
        await self._repo.update_status(
            tenant_id, TenantStatus.TERMINATED,
            terminated_at=datetime.now(timezone.utc).isoformat(),
        )

    async def upgrade_plan(self, tenant_id: int, new_plan: TenantPlan) -> None:
        from api.modules.tenancy.models.quota_event import QuotaEventType
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
        await self._repo.update_plan(tenant_id, new_plan)
        await self._repo.log_quota_event(
            tenant_id, QuotaEventType.PLAN_UPGRADED,
            old_value=list(_PLAN_LIMITS.keys()).index(tenant.plan),
            new_value=list(_PLAN_LIMITS.keys()).index(new_plan),
            note=f"{tenant.plan} → {new_plan}",
        )

    async def enable_module(self, tenant_id: int, module: str) -> None:
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
        modules = list(tenant.enabled_modules or [])
        if module not in modules:
            modules.append(module)
        from sqlalchemy import update
        from api.modules.tenancy.models.tenant import Tenant as T
        from sqlalchemy.ext.asyncio import AsyncSession
        await self._repo._s.execute(
            update(T).where(T.id == tenant_id).values(enabled_modules=modules)
        )
        await self._repo._s.flush()

    async def disable_module(self, tenant_id: int, module: str) -> None:
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
        modules = [m for m in (tenant.enabled_modules or []) if m != module]
        from sqlalchemy import update
        from api.modules.tenancy.models.tenant import Tenant as T
        await self._repo._s.execute(
            update(T).where(T.id == tenant_id).values(enabled_modules=modules)
        )
        await self._repo._s.flush()
