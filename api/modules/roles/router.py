"""Roles module — aggregates role and assignment routers."""
from fastapi import APIRouter
from api.modules.roles.routers.role_router import router as role_router
from api.modules.roles.routers.assignment_router import router as assignment_router

router = APIRouter()
router.include_router(role_router)
router.include_router(assignment_router)
