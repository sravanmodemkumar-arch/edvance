"""Tenancy module — aggregates all sub-routers."""
from fastapi import APIRouter
from api.modules.tenancy.routers.admin_router import router as admin_router
from api.modules.tenancy.routers.branding_router import router as branding_router
from api.modules.tenancy.routers.public_router import router as public_router
from api.modules.tenancy.routers.cache_router import router as cache_router

router = APIRouter()
router.include_router(public_router)
router.include_router(branding_router)
router.include_router(admin_router)
router.include_router(cache_router)
