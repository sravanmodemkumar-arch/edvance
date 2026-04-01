"""Finance routers — fee_structure, fee_collection, fee_defaulters, payroll, payment_gateway."""
from fastapi import APIRouter
from api.modules.fee_structure.router import router as fee_structure_router
from api.modules.fee_collection.router import router as fee_collection_router
from api.modules.fee_defaulters.router import router as fee_defaulters_router
from api.modules.payroll.router import router as payroll_router
from api.modules.payment_gateway.router import router as payment_router

router = APIRouter()
router.include_router(fee_structure_router, prefix="/fee-structures", tags=["finance"])
router.include_router(fee_collection_router, prefix="/fee-collections", tags=["finance"])
router.include_router(fee_defaulters_router, prefix="/fee-defaulters", tags=["finance"])
router.include_router(payroll_router, prefix="/payroll", tags=["finance"])
router.include_router(payment_router, prefix="/payments", tags=["finance"])
