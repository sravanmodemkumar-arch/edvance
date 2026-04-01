"""Documents + compliance routers — certificates, documents, pocso, dpdpa, compliance."""
from fastapi import APIRouter
from api.modules.certificates.router import router as certificates_router
from api.modules.documents.router import router as documents_router
from api.modules.pocso.router import router as pocso_router
from api.modules.dpdpa.router import router as dpdpa_router
from api.modules.compliance.router import router as compliance_router

router = APIRouter()
router.include_router(certificates_router, prefix="/certificates", tags=["docs"])
router.include_router(documents_router, prefix="/documents", tags=["docs"])
router.include_router(pocso_router, prefix="/pocso", tags=["compliance"])
router.include_router(dpdpa_router, prefix="/dpdpa", tags=["compliance"])
router.include_router(compliance_router, prefix="/compliance", tags=["compliance"])
