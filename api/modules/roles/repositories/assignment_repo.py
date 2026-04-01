"""Role assignment and delegation data access."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.roles.models.assignment import RoleAssignment, RoleDelegation


class AssignmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def assign(
        self,
        tenant_id: int,
        user_id: int,
        role_id: int,
        role_code: str,
        assigned_by_id: int,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        scope_context: dict | None = None,
    ) -> RoleAssignment:
        assignment = RoleAssignment(
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role_id,
            role_code=role_code,
            assigned_by_id=assigned_by_id,
            starts_at=starts_at,
            ends_at=ends_at,
            scope_context=scope_context,
            is_active=True,
        )
        self._s.add(assignment)
        await self._s.flush()
        return assignment

    async def get_active_for_user(self, tenant_id: int, user_id: int) -> list[RoleAssignment]:
        now = datetime.now(timezone.utc)
        r = await self._s.execute(
            select(RoleAssignment).where(
                RoleAssignment.tenant_id == tenant_id,
                RoleAssignment.user_id == user_id,
                RoleAssignment.is_active.is_(True),
            )
        )
        assignments = list(r.scalars().all())
        # Filter time-bound — those not yet started or already expired
        return [
            a for a in assignments
            if (a.starts_at is None or a.starts_at <= now)
            and (a.ends_at is None or a.ends_at >= now)
        ]

    async def revoke(self, assignment_id: int, revoked_by_id: int) -> None:
        await self._s.execute(
            update(RoleAssignment)
            .where(RoleAssignment.id == assignment_id)
            .values(is_active=False)
        )
        await self._s.flush()

    async def expire_overdue(self, tenant_id: int) -> list[int]:
        """Expire all assignments where ends_at has passed. Returns user_ids affected."""
        now = datetime.now(timezone.utc)
        r = await self._s.execute(
            select(RoleAssignment).where(
                RoleAssignment.tenant_id == tenant_id,
                RoleAssignment.is_active.is_(True),
                RoleAssignment.ends_at < now,
                RoleAssignment.ends_at.isnot(None),
            )
        )
        expired = list(r.scalars().all())
        for a in expired:
            a.is_active = False
        await self._s.flush()
        return list({a.user_id for a in expired})

    async def acknowledge(self, assignment_id: int) -> None:
        await self._s.execute(
            update(RoleAssignment)
            .where(RoleAssignment.id == assignment_id)
            .values(acknowledged_at=datetime.now(timezone.utc))
        )
        await self._s.flush()

    # ─── Delegations ─────────────────────────────────────────────────────────

    async def create_delegation(self, **kwargs) -> RoleDelegation:
        d = RoleDelegation(**kwargs)
        self._s.add(d)
        await self._s.flush()
        return d

    async def get_active_delegations_for(self, user_id: int, tenant_id: int) -> list[RoleDelegation]:
        now = datetime.now(timezone.utc)
        r = await self._s.execute(
            select(RoleDelegation).where(
                RoleDelegation.delegate_user_id == user_id,
                RoleDelegation.tenant_id == tenant_id,
                RoleDelegation.is_active.is_(True),
                RoleDelegation.starts_at <= now,
                RoleDelegation.ends_at >= now,
            )
        )
        return list(r.scalars().all())
