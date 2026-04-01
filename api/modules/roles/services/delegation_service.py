"""Delegation — time-bound authority transfer with full audit trail."""
from __future__ import annotations
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.roles.permissions import get_permissions, has_permission
from api.modules.roles.repositories.assignment_repo import AssignmentRepository
from api.modules.roles.repositories.role_repo import RoleRepository


class DelegationService:
    def __init__(self, session: AsyncSession) -> None:
        self._assign_repo = AssignmentRepository(session)
        self._role_repo = RoleRepository(session)

    async def create_delegation(
        self,
        *,
        tenant_id: int,
        delegator_user_id: int,
        delegator_roles: list[str],
        delegate_user_id: int,
        permissions_to_delegate: list[str],
        starts_at: datetime,
        ends_at: datetime,
        reason: str | None = None,
    ) -> None:
        if ends_at <= starts_at:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                "ends_at must be after starts_at")

        # Validate delegator actually holds the permissions they're delegating
        delegator_perms = get_permissions(delegator_roles)
        for perm in permissions_to_delegate:
            parts = perm.split(":")
            if len(parts) != 3:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    f"Invalid permission format: {perm}")
            mod, action, scope = parts
            if not has_permission(delegator_perms, mod, action, scope):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    f"Cannot delegate permission you don't hold: {perm}",
                )

        await self._assign_repo.create_delegation(
            tenant_id=tenant_id,
            delegator_user_id=delegator_user_id,
            delegate_user_id=delegate_user_id,
            role_code="DELEGATED",
            permissions=permissions_to_delegate,
            starts_at=starts_at,
            ends_at=ends_at,
            reason=reason,
        )

    async def get_delegated_permissions(self, user_id: int, tenant_id: int) -> set[str]:
        """Return all currently active delegated permissions for a user."""
        delegations = await self._assign_repo.get_active_delegations_for(user_id, tenant_id)
        perms: set[str] = set()
        for d in delegations:
            perms |= set(d.permissions)
        return perms
