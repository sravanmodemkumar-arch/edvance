"""Identity service — FastAPI app entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.middleware.tenant import TenantMiddleware
from app.api.v1 import router as v1_router
import os

app = FastAPI(
    title="Edvance Identity Service",
    version="1.0.0",
    docs_url="/docs" if os.getenv("APP_ENV") != "production" else None,
)

app.add_middleware(TenantMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "identity"}
