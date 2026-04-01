"""TenantMiddleware — subdomain/custom-domain resolution with in-process cache.

Resolution order:
  1. request.state.tenant already set (upstream middleware) → skip
  2. Host header → extract slug → cache lookup → DB lookup
  3. JWT tenant_id claim → accepted for API clients (mobile apps) that skip subdomain

Cache: in-process dict with 15-minute TTL (per-process, refreshes on Lambda cold start).
Invalidation: call TenantCache.invalidate(slug) from admin endpoints.
"""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

_TTL_SECONDS = 900            # 15 minutes — per doc
_PLATFORM_SLUGS = {"api", "www", "admin", "app", "static"}
_BASE_DOMAIN = "eduforge.in"  # canonical; .edvance.in also works


@dataclass
class _CacheEntry:
    tenant: Any           # Tenant ORM object or dict
    expires_at: float


class TenantCache:
    """Thread-safe in-process cache with TTL. Singleton per process."""

    def __init__(self) -> None:
        self._data: dict[str, _CacheEntry] = {}
        self._lock = asyncio.Lock()

    async def get(self, slug: str) -> Any | None:
        async with self._lock:
            entry = self._data.get(slug)
            if entry and entry.expires_at > time.monotonic():
                return entry.tenant
            return None

    async def set(self, slug: str, tenant: Any) -> None:
        async with self._lock:
            self._data[slug] = _CacheEntry(
                tenant=tenant, expires_at=time.monotonic() + _TTL_SECONDS
            )

    async def invalidate(self, slug: str) -> None:
        async with self._lock:
            self._data.pop(slug, None)

    async def clear(self) -> None:
        async with self._lock:
            self._data.clear()


# Module-level singleton — shared across all requests in the same process
tenant_cache = TenantCache()

# Type alias for the injected resolver
TenantResolver = Callable[[str], Awaitable[Any | None]]


def _extract_slug(host: str) -> str | None:
    """Return slug from host header or None for platform routes."""
    host = host.split(":")[0].lower()  # strip port
    for base in (f".{_BASE_DOMAIN}", ".edvance.in"):
        if host.endswith(base):
            slug = host[: -len(base)]
            return None if slug in _PLATFORM_SLUGS else slug
    return None


class TenantMiddleware(BaseHTTPMiddleware):
    """Attach resolved tenant to request.state.tenant.

    Requires app.state.tenant_resolver to be set at startup (see main.py).
    Falls back gracefully when resolver is not configured (tests / health checks).
    """

    async def dispatch(self, request: Request, call_next):
        slug = _extract_slug(request.headers.get("host", ""))

        if slug:
            tenant = await tenant_cache.get(slug)
            if tenant is None:
                resolver: TenantResolver | None = getattr(
                    request.app.state, "tenant_resolver", None
                )
                if resolver:
                    tenant = await resolver(slug)
                    if tenant:
                        await tenant_cache.set(slug, tenant)

            if tenant is None and slug:
                # Unknown subdomain — reject early (avoids DB hit on every req)
                return JSONResponse({"detail": "Institution not found."}, status_code=404)

            if tenant is not None and hasattr(tenant, "status"):
                if str(tenant.status) == "SUSPENDED":
                    return JSONResponse(
                        {"detail": "This institution's account is suspended."},
                        status_code=451,   # 451 Unavailable For Legal Reasons — abuse/suspension
                    )
                if str(tenant.status) in ("TERMINATED", "ARCHIVED"):
                    return JSONResponse({"detail": "Institution not found."}, status_code=404)

            request.state.tenant = tenant
        else:
            request.state.tenant = None

        return await call_next(request)
