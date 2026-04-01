"""Public tenant info — unauthenticated. Used by login page to load branding."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.modules.tenancy.models.tenant import Tenant
from api.modules.tenancy.repositories.tenant_repo import TenantRepository
from api.modules.tenancy.schemas.tenant_schema import TenantPublic

router = APIRouter(prefix="/tenants", tags=["tenancy"])


@router.get("/{slug}/public", response_model=TenantPublic)
async def get_tenant_public(slug: str, db: AsyncSession = Depends(get_db)):
    """Returns branding + enabled modules for the login page.
    Never exposes DB host, plan details, or admin contact.
    """
    repo = TenantRepository(db)
    tenant = await repo.get_by_slug(slug)
    if tenant is None:
        from fastapi import HTTPException, status
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Institution not found")
    return TenantPublic.model_validate(tenant)
