"""Role data access."""
from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.roles.models.role import Role, RoleChangeLog, RoleGroup


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, role_id: int) -> Role | None:
        return await self._s.get(Role, role_id)

    async def get_by_code(self, code: str, tenant_id: int) -> Role | None:
        r = await self._s.execute(
            select(Role).where(Role.code == code, Role.tenant_id == tenant_id)
        )
        return r.scalar_one_or_none()

    async def list_for_tenant(self, tenant_id: int) -> list[Role]:
        r = await self._s.execute(
            select(Role).where(Role.tenant_id == tenant_id, Role.is_active.is_(True))
        )
        return list(r.scalars().all())

    async def create_custom(
        self,
        tenant_id: int,
        name: str,
        code: str,
        role_group: RoleGroup,
        hierarchy_level: int,
        permissions: list[str],
        description: str | None = None,
    ) -> Role:
        role = Role(
            tenant_id=tenant_id,
            name=name,
            code=code,
            role_group=role_group,
            hierarchy_level=hierarchy_level,
            is_system=False,
            permissions=permissions,
            description=description,
        )
        self._s.add(role)
        await self._s.flush()
        return role

    async def approve(self, role_id: int, approver_id: int) -> None:
        from sqlalchemy import update
        from datetime import datetime, timezone
        await self._s.execute(
            update(Role).where(Role.id == role_id).values(
                is_active=True,
                approved_by=approver_id,
                approved_at=datetime.now(timezone.utc),
            )
        )
        await self._s.flush()

    async def log_change(self, **kwargs) -> None:
        self._s.add(RoleChangeLog(**kwargs))
        await self._s.flush()

    async def list_change_log(self, tenant_id: int, user_id: int) -> list[RoleChangeLog]:
        r = await self._s.execute(
            select(RoleChangeLog).where(
                RoleChangeLog.tenant_id == tenant_id,
                RoleChangeLog.target_user_id == user_id,
            ).order_by(RoleChangeLog.created_at.desc())
        )
        return list(r.scalars().all())
