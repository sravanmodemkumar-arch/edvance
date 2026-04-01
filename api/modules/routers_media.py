"""Media routers — video, live_classes."""
from fastapi import APIRouter
from api.modules.video.router import router as video_router
from api.modules.live_classes.router import router as live_classes_router

router = APIRouter()
router.include_router(video_router, prefix="/videos", tags=["media"])
router.include_router(live_classes_router, prefix="/live-classes", tags=["media"])
