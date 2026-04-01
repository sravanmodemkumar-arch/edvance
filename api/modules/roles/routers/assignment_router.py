"""Role assignment, revocation, delegation, acknowledgement endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.dependencies import CurrentUser
from api.modules.roles.dependencies import require_permission
from api.modules.roles.repositories.assignment_repo import AssignmentRepository
from api.modules.roles.schemas.role_schema import (
    AcknowledgeRequest, AssignRoleRequest, DelegationCreate, RevokeRoleRequest,
)
from api.modules.roles.services.delegation_service import DelegationService
from api.modules.roles.services.rbac_service import RBACService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/assign", status_code=status.HTTP_201_CREATED)
async def assign_role(
    body: AssignRoleRequest,
    current_user: CurrentUser,
    _perm=Depends(require_permission("roles", "create", "dept")),
    db: AsyncSession = Depends(get_db),
):
    from api.modules.auth.repositories.user_repo import UserRepository
    svc = RBACService(db)
    user_repo = UserRepository(db)
    assigner = await user_repo.get_by_uid(current_user.sub)
    await svc.assign_role(
        tenant_id=int(current_user.tenant_id),
        target_user_id=body.target_user_id,
        role_code=body.role_code,
        assigner_user_id=assigner.id,
        assigner_roles=current_user.roles,
        starts_at=body.starts_at,
        ends_at=body.ends_at,
        scope_context=body.scope_context,
        reason=body.reason,
    )
    return {"detail": f"Role '{body.role_code}' assigned successfully"}


@router.post("/revoke", status_code=status.HTTP_200_OK)
async def revoke_role(
    body: RevokeRoleRequest,
    current_user: CurrentUser,
    _perm=Depends(require_permission("roles", "edit", "dept")),
    db: AsyncSession = Depends(get_db),
):
    from api.modules.auth.repositories.user_repo import UserRepository
    svc = RBACService(db)
    user_repo = UserRepository(db)
    revoker = await user_repo.get_by_uid(current_user.sub)
    await svc.revoke_role(
        assignment_id=body.assignment_id,
        tenant_id=int(current_user.tenant_id),
        target_user_id=body.target_user_id,
        role_code=body.role_code,
        revoker_user_id=revoker.id,
        revoker_roles=current_user.roles,
        reason=body.reason,
    )
    return {"detail": "Role revoked"}


@router.post("/acknowledge", status_code=status.HTTP_200_OK)
async def acknowledge_assignment(
    body: AcknowledgeRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Staff acknowledges their role assignment within 48 hours."""
    repo = AssignmentRepository(db)
    await repo.acknowledge(body.assignment_id)
    return {"detail": "Role assignment acknowledged"}


@router.post("/delegate", status_code=status.HTTP_201_CREATED)
async def delegate_authority(
    body: DelegationCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = DelegationService(db)
    await svc.create_delegation(
        tenant_id=int(current_user.tenant_id),
        delegator_user_id=int(current_user.sub.split("_")[-1]) if "_" in current_user.sub else 0,
        delegator_roles=current_user.roles,
        delegate_user_id=body.delegate_user_id,
        permissions_to_delegate=body.permissions,
        starts_at=body.starts_at,
        ends_at=body.ends_at,
        reason=body.reason,
    )
    return {"detail": "Authority delegated successfully"}
