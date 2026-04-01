"""Role CRUD — list system roles, create/approve custom roles."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.dependencies import CurrentUser
from api.modules.roles.dependencies import require_permission
from api.modules.roles.models.role import RoleGroup
from api.modules.roles.repositories.role_repo import RoleRepository
from api.modules.roles.schemas.role_schema import CustomRoleCreate, RoleOut
from api.modules.roles.services.rbac_service import RBACService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleOut])
async def list_roles(
    current_user: CurrentUser,
    _perm=Depends(require_permission("roles", "view", "institution")),
    db: AsyncSession = Depends(get_db),
):
    repo = RoleRepository(db)
    roles = await repo.list_for_tenant(int(current_user.tenant_id))
    return [RoleOut.model_validate(r) for r in roles]


@router.post("", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_custom_role(
    body: CustomRoleCreate,
    current_user: CurrentUser,
    _perm=Depends(require_permission("roles", "create", "institution")),
    db: AsyncSession = Depends(get_db),
):
    """Creates a custom role in PENDING state. Requires Principal approval."""
    repo = RoleRepository(db)
    role = await repo.create_custom(
        tenant_id=int(current_user.tenant_id),
        name=body.name, code=body.code,
        role_group=body.role_group,
        hierarchy_level=body.hierarchy_level,
        permissions=body.permissions,
        description=body.description,
    )
    # Custom roles start inactive until Principal approves
    role.is_active = False
    return RoleOut.model_validate(role)


@router.post("/{role_id}/approve", status_code=status.HTTP_200_OK)
async def approve_custom_role(
    role_id: int,
    current_user: CurrentUser,
    _perm=Depends(require_permission("roles", "approve", "institution")),
    db: AsyncSession = Depends(get_db),
):
    """Principal approves a pending custom role."""
    from api.modules.auth.repositories.user_repo import UserRepository
    user_repo = UserRepository(db)
    user = await user_repo.get_by_uid(current_user.sub)
    repo = RoleRepository(db)
    await repo.approve(role_id, user.id)
    return {"detail": "Role approved and activated"}
