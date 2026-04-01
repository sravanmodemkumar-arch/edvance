"""Operations routers — hostel, transport, library, admission, counselling, ptm."""
from fastapi import APIRouter
from api.modules.hostel.router import router as hostel_router
from api.modules.transport.router import router as transport_router
from api.modules.library.router import router as library_router
from api.modules.admission.router import router as admission_router
from api.modules.counselling.router import router as counselling_router
from api.modules.ptm.router import router as ptm_router

router = APIRouter()
router.include_router(hostel_router, prefix="/hostel", tags=["ops"])
router.include_router(transport_router, prefix="/transport", tags=["ops"])
router.include_router(library_router, prefix="/library", tags=["ops"])
router.include_router(admission_router, prefix="/admissions", tags=["ops"])
router.include_router(counselling_router, prefix="/counselling", tags=["ops"])
router.include_router(ptm_router, prefix="/ptm", tags=["ops"])
