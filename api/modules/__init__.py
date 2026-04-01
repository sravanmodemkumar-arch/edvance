"""Main router aggregator — includes all 11 sub-routers (57 modules total)."""
from fastapi import APIRouter
from api.modules.routers_identity import router as identity_router
from api.modules.routers_institution import router as institution_router
from api.modules.routers_academic import router as academic_router
from api.modules.routers_exam import router as exam_router
from api.modules.routers_finance import router as finance_router
from api.modules.routers_ops import router as ops_router
from api.modules.routers_comms import router as comms_router
from api.modules.routers_docs import router as docs_router
from api.modules.routers_media import router as media_router
from api.modules.routers_ai import router as ai_router
from api.modules.routers_platform import router as platform_router

router = APIRouter()
router.include_router(identity_router)
router.include_router(institution_router)
router.include_router(academic_router)
router.include_router(exam_router)
router.include_router(finance_router)
router.include_router(ops_router)
router.include_router(comms_router)
router.include_router(docs_router)
router.include_router(media_router)
router.include_router(ai_router)
router.include_router(platform_router)
