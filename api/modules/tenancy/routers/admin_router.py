"""Platform admin CRUD for tenants — PLATFORM_ADMIN role only."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.dependencies import CurrentUser
from api.modules.tenancy.models.tenant import TenantStatus
from api.modules.tenancy.repositories.tenant_repo import TenantRepository
from api.modules.tenancy.schemas.tenant_schema import (
    TenantAdmin, TenantCreate, PlanUpgrade, ModuleToggle, TenantStatusUpdate,
)
from api.modules.tenancy.services.tenant_service import TenantService
from shared.exceptions.auth_exceptions import InsufficientPermissionsError
from shared.middleware.tenant import tenant_cache

router = APIRouter(prefix="/admin/tenants", tags=["tenancy-admin"])


def _require_platform_admin(current_user: CurrentUser) -> None:
    if "PLATFORM_ADMIN" not in current_user.roles:
        raise InsufficientPermissionsError()


@router.post("", response_model=TenantAdmin, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    body: TenantCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    _require_platform_admin(current_user)
    svc = TenantService(db)
    tenant = await svc.provision(
        name=body.name, slug=body.slug, tenant_type=body.tenant_type,
        plan=body.plan, board=body.board,
        academic_year_start_month=body.academic_year_start_month,
        admin_name=body.admin_name, admin_email=body.admin_email,
        admin_mobile=body.admin_mobile,
        udise_code=body.udise_code, gst_number=body.gst_number,
    )
    return TenantAdmin.model_validate(tenant)


@router.get("/{slug}", response_model=TenantAdmin)
async def get_tenant(slug: str, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    _require_platform_admin(current_user)
    repo = TenantRepository(db)
    tenant = await repo.get_by_slug(slug)
    if not tenant:
        from fastapi import HTTPException
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return TenantAdmin.model_validate(tenant)


@router.patch("/{slug}/status", status_code=status.HTTP_200_OK)
async def update_status(
    slug: str, body: TenantStatusUpdate,
    current_user: CurrentUser, db: AsyncSession = Depends(get_db),
):
    _require_platform_admin(current_user)
    svc = TenantService(db)
    repo = TenantRepository(db)
    tenant = await repo.get_by_slug(slug)
    if not tenant:
        from fastapi import HTTPException
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    transitions = {
        TenantStatus.ACTIVE: svc.activate,
        TenantStatus.WARNING: svc.warn,
        TenantStatus.SUSPENDED: svc.suspend,
        TenantStatus.TERMINATED: svc.terminate,
    }
    fn = transitions.get(body.status)
    if fn:
        await fn(tenant.id)
    await tenant_cache.invalidate(slug)
    return {"detail": f"Status updated to {body.status}"}


@router.patch("/{slug}/plan", status_code=status.HTTP_200_OK)
async def upgrade_plan(
    slug: str, body: PlanUpgrade,
    current_user: CurrentUser, db: AsyncSession = Depends(get_db),
):
    _require_platform_admin(current_user)
    repo = TenantRepository(db)
    tenant = await repo.get_by_slug(slug)
    if not tenant:
        from fastapi import HTTPException
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    svc = TenantService(db)
    await svc.upgrade_plan(tenant.id, body.plan)
    await tenant_cache.invalidate(slug)
    return {"detail": f"Plan upgraded to {body.plan}"}


@router.patch("/{slug}/modules", status_code=status.HTTP_200_OK)
async def toggle_module(
    slug: str, body: ModuleToggle,
    current_user: CurrentUser, db: AsyncSession = Depends(get_db),
):
    _require_platform_admin(current_user)
    repo = TenantRepository(db)
    tenant = await repo.get_by_slug(slug)
    if not tenant:
        from fastapi import HTTPException
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    svc = TenantService(db)
    if body.enabled:
        await svc.enable_module(tenant.id, body.module)
    else:
        await svc.disable_module(tenant.id, body.module)
    await tenant_cache.invalidate(slug)
    return {"detail": f"Module '{body.module}' {'enabled' if body.enabled else 'disabled'}"}
