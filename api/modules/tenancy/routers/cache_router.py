"""Cache management — force-invalidate tenant cache entries.

Called after EduForge admin changes branding, plan, or status so all
API instances serve fresh data immediately (without waiting 15-min TTL).
Internal endpoint — platform admin only.
"""
from fastapi import APIRouter, Depends, status
from api.core.dependencies import CurrentUser
from shared.exceptions.auth_exceptions import InsufficientPermissionsError
from shared.middleware.tenant import tenant_cache

router = APIRouter(prefix="/admin/cache", tags=["tenancy-admin"])


@router.delete("/tenant/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def invalidate_tenant_cache(slug: str, current_user: CurrentUser):
    if "PLATFORM_ADMIN" not in current_user.roles:
        raise InsufficientPermissionsError()
    await tenant_cache.invalidate(slug)


@router.delete("/tenants", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_tenant_cache(current_user: CurrentUser):
    if "PLATFORM_ADMIN" not in current_user.roles:
        raise InsufficientPermissionsError()
    await tenant_cache.clear()
