"""Academic routers — timetable, attendance (3 types), homework, syllabus, notes."""
from fastapi import APIRouter
from api.modules.timetable.router import router as timetable_router
from api.modules.attendance_school.router import router as att_school_router
from api.modules.attendance_coaching.router import router as att_coaching_router
from api.modules.attendance_hostel.router import router as att_hostel_router
from api.modules.homework.router import router as homework_router
from api.modules.syllabus.router import router as syllabus_router
from api.modules.notes.router import router as notes_router

router = APIRouter()
router.include_router(timetable_router, prefix="/timetable", tags=["timetable"])
router.include_router(att_school_router, prefix="/attendance/school", tags=["attendance"])
router.include_router(att_coaching_router, prefix="/attendance/coaching", tags=["attendance"])
router.include_router(att_hostel_router, prefix="/attendance/hostel", tags=["attendance"])
router.include_router(homework_router, prefix="/homework", tags=["homework"])
router.include_router(syllabus_router, prefix="/syllabus", tags=["syllabus"])
router.include_router(notes_router, prefix="/notes", tags=["notes"])
