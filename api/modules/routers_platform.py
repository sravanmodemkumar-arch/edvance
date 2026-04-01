"""Platform routers — catalog, subscriptions, b2b, white_label, analytics, flags, incident, billing."""
from fastapi import APIRouter
from api.modules.exam_catalog.router import router as catalog_router
from api.modules.subscriptions.router import router as subscriptions_router
from api.modules.b2b_api.router import router as b2b_router
from api.modules.white_label.router import router as white_label_router
from api.modules.platform_analytics.router import router as platform_analytics_router
from api.modules.feature_flags.router import router as feature_flags_router
from api.modules.incident.router import router as incident_router
from api.modules.platform_billing.router import router as platform_billing_router

router = APIRouter()
router.include_router(catalog_router, prefix="/exam-catalog", tags=["platform"])
router.include_router(subscriptions_router, prefix="/subscriptions", tags=["platform"])
router.include_router(b2b_router, prefix="/b2b", tags=["platform"])
router.include_router(white_label_router, prefix="/white-label", tags=["platform"])
router.include_router(platform_analytics_router, prefix="/platform/analytics", tags=["platform"])
router.include_router(feature_flags_router, prefix="/feature-flags", tags=["platform"])
router.include_router(incident_router, prefix="/incidents", tags=["platform"])
router.include_router(platform_billing_router, prefix="/platform/billing", tags=["platform"])
