"""Roles routers."""
from .role_router import router as role_router
from .assignment_router import router as assignment_router

__all__ = ["role_router", "assignment_router"]
