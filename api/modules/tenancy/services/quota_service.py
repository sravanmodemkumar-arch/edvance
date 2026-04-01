"""Quota enforcement — student/staff counts and storage limits.

Called by: student enrolment, staff management, file upload modules.
Raises HTTP 402 when hard limit is crossed (plan auto-upgrade trigger).
"""
from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.tenancy.models.quota_event import QuotaEventType
from api.modules.tenancy.repositories.tenant_repo import TenantRepository

_SOFT_THRESHOLD = 0.90   # 90% → warning event
_STORAGE_SOFT_THRESHOLD = 0.80   # 80% → storage warning


class QuotaService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TenantRepository(session)

    async def check_and_add_student(self, tenant_id: int, actor_id: int | None = None) -> None:
        """Increment student count. Raises 402 if hard limit crossed."""
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")

        new_count = await self._repo.increment_students(tenant_id)

        # Hard limit
        if new_count > tenant.max_students:
            await self._repo.log_quota_event(
                tenant_id, QuotaEventType.HARD_LIMIT_REACHED,
                old_value=tenant.max_students, new_value=new_count, actor_id=actor_id,
            )
            raise HTTPException(
                status.HTTP_402_PAYMENT_REQUIRED,
                f"Student limit ({tenant.max_students}) reached. Upgrade plan.",
            )

        # Soft limit
        ratio = new_count / tenant.max_students
        if ratio >= _SOFT_THRESHOLD and (new_count - 1) / tenant.max_students < _SOFT_THRESHOLD:
            await self._repo.log_quota_event(
                tenant_id, QuotaEventType.SOFT_LIMIT_WARNING,
                old_value=tenant.max_students, new_value=new_count, actor_id=actor_id,
                note=f"90% student quota reached ({new_count}/{tenant.max_students})",
            )

        await self._repo.log_quota_event(
            tenant_id, QuotaEventType.STUDENT_ADDED,
            new_value=new_count, actor_id=actor_id,
        )

    async def remove_student(self, tenant_id: int, actor_id: int | None = None) -> None:
        await self._repo.increment_students(tenant_id, delta=-1)
        tenant = await self._repo.get_by_id(tenant_id)
        await self._repo.log_quota_event(
            tenant_id, QuotaEventType.STUDENT_REMOVED,
            new_value=tenant.current_students if tenant else None, actor_id=actor_id,
        )

    async def check_and_add_staff(self, tenant_id: int, actor_id: int | None = None) -> None:
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")

        new_count = await self._repo.increment_staff(tenant_id)
        if new_count > tenant.max_staff:
            raise HTTPException(
                status.HTTP_402_PAYMENT_REQUIRED,
                f"Staff limit ({tenant.max_staff}) reached. Upgrade plan.",
            )
        await self._repo.log_quota_event(
            tenant_id, QuotaEventType.STAFF_ADDED, new_value=new_count, actor_id=actor_id,
        )

    async def check_and_add_storage(self, tenant_id: int, size_mb: int) -> None:
        tenant = await self._repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")

        storage_limit_mb = tenant.storage_gb * 1024
        new_used = await self._repo.add_storage_mb(tenant_id, size_mb)

        if new_used > storage_limit_mb:
            await self._repo.log_quota_event(tenant_id, QuotaEventType.STORAGE_FULL)
            raise HTTPException(
                status.HTTP_402_PAYMENT_REQUIRED,
                "Storage limit reached. Upgrade plan or delete files.",
            )

        ratio = new_used / storage_limit_mb
        if ratio >= _STORAGE_SOFT_THRESHOLD and (new_used - size_mb) / storage_limit_mb < _STORAGE_SOFT_THRESHOLD:
            await self._repo.log_quota_event(
                tenant_id, QuotaEventType.STORAGE_WARNING,
                note=f"80% storage used ({new_used}MB / {storage_limit_mb}MB)",
            )
