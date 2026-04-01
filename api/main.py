"""Edvance API — FastAPI app entry point.

Compute targets (zero code changes between them):
  Phase 1: uvicorn api.main:app  (VPS behind CF Tunnel)
  Phase 2: handler = Mangum(app) (AWS Lambda)
  Phase 3: handler = Mangum(app) (AWS Lambda)
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from shared.middleware.tenant import TenantMiddleware
from shared.middleware.request_id import RequestIDMiddleware
from api.core.exception_handlers import register_handlers
from api.modules import router as modules_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # startup / shutdown hooks go here


def create_app() -> FastAPI:
    env = os.getenv("APP_ENV", "dev")
    app = FastAPI(
        title="Edvance API",
        version="1.0.0",
        docs_url="/docs" if env != "production" else None,
        redoc_url="/redoc" if env != "production" else None,
        lifespan=lifespan,
    )

    # Middleware — order matters (outermost = last added)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TenantMiddleware)
    app.add_middleware(RequestIDMiddleware)

    register_handlers(app)
    app.include_router(modules_router, prefix="/api/v1")

    @app.get("/health", tags=["ops"])
    async def health():
        return {"status": "ok", "provider": os.getenv("INFRA_PROVIDER", "hybrid")}

    return app


app = create_app()

# AWS Lambda entry point — ignored when running with uvicorn
handler = Mangum(app, lifespan="off")
