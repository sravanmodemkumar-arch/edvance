"""AI routers — ai_doubt, ai_analytics, ai_content."""
from fastapi import APIRouter
from api.modules.ai_doubt.router import router as ai_doubt_router
from api.modules.ai_analytics.router import router as ai_analytics_router
from api.modules.ai_content.router import router as ai_content_router

router = APIRouter()
router.include_router(ai_doubt_router, prefix="/ai/doubt", tags=["ai"])
router.include_router(ai_analytics_router, prefix="/ai/analytics", tags=["ai"])
router.include_router(ai_content_router, prefix="/ai/content", tags=["ai"])
