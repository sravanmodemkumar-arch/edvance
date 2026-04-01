"""Institution routers — institution, branch, academic_year, staff, student, parent."""
from fastapi import APIRouter
from api.modules.institution.router import router as institution_router
from api.modules.branch.router import router as branch_router
from api.modules.academic_year.router import router as academic_year_router
from api.modules.staff.router import router as staff_router
from api.modules.student.router import router as student_router
from api.modules.parent.router import router as parent_router

router = APIRouter()
router.include_router(institution_router, prefix="/institutions", tags=["institution"])
router.include_router(branch_router, prefix="/branches", tags=["branch"])
router.include_router(academic_year_router, prefix="/academic-years", tags=["academic_year"])
router.include_router(staff_router, prefix="/staff", tags=["staff"])
router.include_router(student_router, prefix="/students", tags=["student"])
router.include_router(parent_router, prefix="/parents", tags=["parent"])
