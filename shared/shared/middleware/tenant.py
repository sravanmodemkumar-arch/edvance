"""Tenant resolution middleware — resolves subdomain to tenant_id."""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        tenant_id = self._resolve_tenant(host)
        request.state.tenant_id = tenant_id
        return await call_next(request)

    def _resolve_tenant(self, host: str) -> int | None:
        # {slug}.schools.edvance.in → look up institution by domain
        # Platform routes (edvance.in) → tenant_id = None
        if "edvance.in" not in host:
            return None
        subdomain = host.split(".edvance.in")[0]
        if subdomain in ("edvance", "www", "api"):
            return None
        return subdomain  # resolved to DB ID in service layer
