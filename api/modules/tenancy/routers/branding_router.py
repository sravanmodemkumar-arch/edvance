"""Branding endpoints — tenant admin only (ADMIN role)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.dependencies import CurrentUser
from api.modules.tenancy.dependencies import require_active_tenant
from api.modules.tenancy.models.tenant import Tenant
from api.modules.tenancy.schemas.tenant_schema import BrandingUpdate, HomepageLayoutUpdate
from api.modules.tenancy.services.branding_service import BrandingService
from shared.exceptions.auth_exceptions import InsufficientPermissionsError

router = APIRouter(prefix="/tenants", tags=["tenancy"])


def _require_admin(current_user: CurrentUser) -> None:
    if "ADMIN" not in current_user.roles and "PLATFORM_ADMIN" not in current_user.roles:
        raise InsufficientPermissionsError()


@router.get("/me/branding")
async def get_branding(
    current_user: CurrentUser,
    tenant: Tenant = Depends(require_active_tenant),
    db: AsyncSession = Depends(get_db),
):
    svc = BrandingService(db)
    return await svc.get_branding(tenant.id)


@router.patch("/me/branding", status_code=status.HTTP_200_OK)
async def update_branding(
    body: BrandingUpdate,
    current_user: CurrentUser,
    tenant: Tenant = Depends(require_active_tenant),
    db: AsyncSession = Depends(get_db),
):
    _require_admin(current_user)
    svc = BrandingService(db)
    await svc.update_branding(
        tenant.id,
        logo_url=body.logo_url,
        primary_color=body.primary_color,
        secondary_color=body.secondary_color,
        font_family=body.font_family,
    )
    # Invalidate cache so next request picks up new branding
    from shared.middleware.tenant import tenant_cache
    await tenant_cache.invalidate(tenant.slug)
    return {"detail": "Branding updated"}


@router.put("/me/homepage-layout", status_code=status.HTTP_200_OK)
async def update_homepage_layout(
    body: HomepageLayoutUpdate,
    current_user: CurrentUser,
    tenant: Tenant = Depends(require_active_tenant),
    db: AsyncSession = Depends(get_db),
):
    _require_admin(current_user)
    svc = BrandingService(db)
    await svc.update_homepage_layout(tenant.id, {"sections": body.sections})
    from shared.middleware.tenant import tenant_cache
    await tenant_cache.invalidate(tenant.slug)
    return {"detail": "Homepage layout updated"}
