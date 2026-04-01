"""RBAC service — role assignment, hierarchy enforcement, audit logging."""
from __future__ import annotations
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.roles.models.role import RoleGroup
from api.modules.roles.permissions import PERMISSION_MAP, get_permissions
from api.modules.roles.repositories.role_repo import RoleRepository
from api.modules.roles.repositories.assignment_repo import AssignmentRepository

# Hierarchy level — lower number = higher authority. MUST NOT assign same or higher.
_HIERARCHY: dict[str, int] = {
    "PLATFORM_ADMIN": 0,
    "GROUP_ADMIN": 5,
    "MANAGEMENT": 10,
    "PRINCIPAL": 20,
    "OWNER": 20,
    "VICE_PRINCIPAL": 25,
    "DEAN": 25,
    "HOD": 30, "EXAM_CELL_HEAD": 30, "ACADEMIC_HEAD": 30,
    "CENTER_DIRECTOR": 30,
    "CLASS_TEACHER": 40, "SUBJECT_TEACHER": 40,
    "PROFESSOR": 40, "LAB_INCHARGE": 40,
    "BATCH_COORDINATOR": 40, "FACULTY": 40,
    "LIBRARIAN": 45, "ACCOUNTANT": 45, "COUNSELLOR": 45,
    "NURSE": 45, "HOSTEL_WARDEN": 45,
    "GATE_STAFF": 50, "TSP_ADMIN": 50,
    "STUDENT": 80, "PARENT": 80,
    "B2B_PARTNER": 90,
    "ALUMNI": 99,
}


class RBACService:
    def __init__(self, session: AsyncSession) -> None:
        self._role_repo = RoleRepository(session)
        self._assign_repo = AssignmentRepository(session)

    def _assigner_level(self, assigner_roles: list[str]) -> int:
        return min((_HIERARCHY.get(r.upper(), 99) for r in assigner_roles), default=99)

    def _target_level(self, role_code: str) -> int:
        return _HIERARCHY.get(role_code.upper(), 99)

    async def assign_role(
        self,
        *,
        tenant_id: int,
        target_user_id: int,
        role_code: str,
        assigner_user_id: int,
        assigner_roles: list[str],
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        scope_context: dict | None = None,
        reason: str | None = None,
    ) -> None:
        # Hierarchy enforcement
        if self._assigner_level(assigner_roles) >= self._target_level(role_code):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Cannot assign a role at or above your own hierarchy level",
            )
        role = await self._role_repo.get_by_code(role_code, tenant_id)
        if not role:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Role '{role_code}' not found")

        assignment = await self._assign_repo.assign(
            tenant_id=tenant_id, user_id=target_user_id,
            role_id=role.id, role_code=role_code,
            assigned_by_id=assigner_user_id,
            starts_at=starts_at, ends_at=ends_at,
            scope_context=scope_context,
        )
        await self._role_repo.log_change(
            tenant_id=tenant_id, target_user_id=target_user_id,
            changed_by_id=assigner_user_id, action="ASSIGNED",
            role_code=role_code, previous_state=None,
            new_state={"starts_at": str(starts_at), "ends_at": str(ends_at)},
            reason=reason,
        )

    async def revoke_role(
        self,
        *,
        assignment_id: int,
        tenant_id: int,
        target_user_id: int,
        role_code: str,
        revoker_user_id: int,
        revoker_roles: list[str],
        reason: str | None = None,
    ) -> None:
        if self._assigner_level(revoker_roles) >= self._target_level(role_code):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot revoke a role at your level")
        await self._assign_repo.revoke(assignment_id, revoker_user_id)
        await self._role_repo.log_change(
            tenant_id=tenant_id, target_user_id=target_user_id,
            changed_by_id=revoker_user_id, action="REMOVED",
            role_code=role_code, reason=reason,
        )

    async def get_effective_scopes(self, tenant_id: int, user_id: int, roles: list[str]) -> list[str]:
        """Build the scopes[] list to embed in JWT at login.

        Combines system role permissions + custom role permissions from DB.
        """
        perms = get_permissions(roles)   # fast: in-memory lookup

        # Add custom role permissions from DB
        assignments = await self._assign_repo.get_active_for_user(tenant_id, user_id)
        for a in assignments:
            role = await self._role_repo.get_by_id(a.role_id)
            if role and not role.is_system and role.permissions:
                perms |= set(role.permissions)

        return sorted(perms)

    async def get_active_roles(self, tenant_id: int, user_id: int) -> list[str]:
        assignments = await self._assign_repo.get_active_for_user(tenant_id, user_id)
        return [a.role_code for a in assignments]
