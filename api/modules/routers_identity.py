"""Identity routers — auth, tenancy, roles."""
from fastapi import APIRouter
from api.modules.auth.router import router as auth_router
from api.modules.tenancy.router import router as tenancy_router
from api.modules.roles.router import router as roles_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(tenancy_router, prefix="/tenancy", tags=["tenancy"])
router.include_router(roles_router, prefix="/roles", tags=["roles"])
