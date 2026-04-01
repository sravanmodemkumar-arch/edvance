"""Branding — logo, colors, font, homepage layout.

Tenant admin controls branding. EduForge admin controls modules/plan.
"""
from __future__ import annotations
import re
from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.tenancy.models.tenant import Tenant

_HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

_DEFAULT_LAYOUT = {
    "sections": [
        {"type": "hero",          "enabled": True,  "order": 1},
        {"type": "announcements", "enabled": True,  "order": 2},
        {"type": "stats",         "enabled": True,  "order": 3},
        {"type": "quick_links",   "enabled": True,  "order": 4},
        {"type": "contact",       "enabled": False, "order": 5},
    ]
}


class BrandingService:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def update_branding(
        self,
        tenant_id: int,
        *,
        logo_url: str | None = None,
        primary_color: str | None = None,
        secondary_color: str | None = None,
        font_family: str | None = None,
    ) -> None:
        if primary_color and not _HEX_RE.match(primary_color):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid hex color")
        if secondary_color and not _HEX_RE.match(secondary_color):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid hex color")

        values: dict = {}
        if logo_url is not None:
            values["logo_url"] = logo_url
        if primary_color is not None:
            values["primary_color"] = primary_color
        if secondary_color is not None:
            values["secondary_color"] = secondary_color
        if font_family is not None:
            values["font_family"] = font_family

        if values:
            await self._s.execute(
                update(Tenant).where(Tenant.id == tenant_id).values(**values)
            )
            await self._s.flush()

    async def update_homepage_layout(self, tenant_id: int, layout: dict) -> None:
        """Validate section ordering and persist."""
        sections = layout.get("sections", [])
        valid_types = {"hero", "announcements", "stats", "quick_links", "contact", "gallery"}
        for sec in sections:
            if sec.get("type") not in valid_types:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    f"Unknown section type: {sec.get('type')}")
        await self._s.execute(
            update(Tenant).where(Tenant.id == tenant_id).values(homepage_layout=layout)
        )
        await self._s.flush()

    async def get_branding(self, tenant_id: int) -> dict:
        tenant = await self._s.get(Tenant, tenant_id)
        if not tenant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
        return {
            "logo_url": tenant.logo_url,
            "primary_color": tenant.primary_color,
            "secondary_color": tenant.secondary_color,
            "font_family": tenant.font_family,
            "homepage_layout": tenant.homepage_layout or _DEFAULT_LAYOUT,
        }
