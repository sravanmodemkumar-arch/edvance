"""Tenancy routers."""
from .admin_router import router as admin_router
from .branding_router import router as branding_router
from .public_router import router as public_router
from .cache_router import router as cache_router

__all__ = ["admin_router", "branding_router", "public_router", "cache_router"]
