"""Communications routers — announcements, notifications, whatsapp, email, sms."""
from fastapi import APIRouter
from api.modules.announcements.router import router as announcements_router
from api.modules.notifications.router import router as notifications_router
from api.modules.whatsapp.router import router as whatsapp_router
from api.modules.email.router import router as email_router
from api.modules.sms.router import router as sms_router

router = APIRouter()
router.include_router(announcements_router, prefix="/announcements", tags=["comms"])
router.include_router(notifications_router, prefix="/notifications", tags=["comms"])
router.include_router(whatsapp_router, prefix="/whatsapp", tags=["comms"])
router.include_router(email_router, prefix="/email", tags=["comms"])
router.include_router(sms_router, prefix="/sms", tags=["comms"])
