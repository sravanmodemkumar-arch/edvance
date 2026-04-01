"""Module 02 Tenancy tests — slug validation, quota, cache, academic year, branding."""
from __future__ import annotations
import asyncio
import pytest
from pydantic import ValidationError
from unittest.mock import AsyncMock, MagicMock, patch

from api.modules.tenancy.models.tenant import TenantPlan, TenantStatus, _PLAN_LIMITS
from api.modules.tenancy.schemas.tenant_schema import TenantCreate
from shared.utils.academic import current_academic_year, academic_year_bounds
from shared.middleware.tenant import TenantCache, _extract_slug


# ─── Slug validation ──────────────────────────────────────────────────────────

class TestSlugValidation:
    @pytest.mark.parametrize("slug,valid", [
        ("dps-delhi", True),
        ("abc123", True),
        ("resonance-kota", True),
        ("DPS-Delhi", False),      # uppercase not allowed
        ("dps_delhi", False),      # underscore not allowed
        ("ab", False),             # too short (< 3)
        ("-dps", False),           # starts with hyphen
        ("dps-", False),           # ends with hyphen
    ])
    def test_slug_format(self, slug, valid):
        data = {
            "name": "Test School",
            "slug": slug,
            "tenant_type": "SCHOOL",
        }
        if valid:
            obj = TenantCreate(**data)
            assert obj.slug == slug.lower()
        else:
            with pytest.raises(ValidationError):
                TenantCreate(**data)


# ─── Plan limits ──────────────────────────────────────────────────────────────

class TestPlanLimits:
    def test_starter_limits(self):
        limits = _PLAN_LIMITS[TenantPlan.STARTER]
        assert limits["max_students"] == 500
        assert limits["max_staff"] == 50
        assert limits["storage_gb"] == 5

    def test_growth_limits(self):
        limits = _PLAN_LIMITS[TenantPlan.GROWTH]
        assert limits["max_students"] == 5_000

    def test_scale_limits(self):
        limits = _PLAN_LIMITS[TenantPlan.SCALE]
        assert limits["max_students"] == 50_000

    def test_enterprise_is_unlimited(self):
        limits = _PLAN_LIMITS[TenantPlan.ENTERPRISE]
        assert limits["max_students"] > 100_000


# ─── Quota service ────────────────────────────────────────────────────────────

class TestQuotaService:
    @pytest.mark.asyncio
    async def test_student_hard_limit_raises_402(self):
        from api.modules.tenancy.services.quota_service import QuotaService
        from fastapi import HTTPException

        mock_session = AsyncMock()
        svc = QuotaService(mock_session)

        fake_tenant = MagicMock()
        fake_tenant.max_students = 100
        fake_tenant.current_students = 100

        with patch.object(svc._repo, "get_by_id", return_value=fake_tenant), \
             patch.object(svc._repo, "increment_students", return_value=101), \
             patch.object(svc._repo, "log_quota_event", new_callable=AsyncMock):
            with pytest.raises(HTTPException) as exc_info:
                await svc.check_and_add_student(1)
            assert exc_info.value.status_code == 402

    @pytest.mark.asyncio
    async def test_soft_limit_event_at_90_percent(self):
        from api.modules.tenancy.services.quota_service import QuotaService
        from api.modules.tenancy.models.quota_event import QuotaEventType

        mock_session = AsyncMock()
        svc = QuotaService(mock_session)

        fake_tenant = MagicMock()
        fake_tenant.max_students = 100
        fake_tenant.current_students = 89  # pre-add

        logged_events = []

        async def log_event(tid, event_type, **kwargs):
            logged_events.append(event_type)

        with patch.object(svc._repo, "get_by_id", return_value=fake_tenant), \
             patch.object(svc._repo, "increment_students", return_value=90), \
             patch.object(svc._repo, "log_quota_event", side_effect=log_event):
            await svc.check_and_add_student(1)

        assert QuotaEventType.SOFT_LIMIT_WARNING in logged_events
        assert QuotaEventType.STUDENT_ADDED in logged_events

    @pytest.mark.asyncio
    async def test_storage_full_raises_402(self):
        from api.modules.tenancy.services.quota_service import QuotaService
        from fastapi import HTTPException

        mock_session = AsyncMock()
        svc = QuotaService(mock_session)

        fake_tenant = MagicMock()
        fake_tenant.storage_gb = 5
        storage_limit_mb = 5 * 1024

        with patch.object(svc._repo, "get_by_id", return_value=fake_tenant), \
             patch.object(svc._repo, "add_storage_mb", return_value=storage_limit_mb + 1), \
             patch.object(svc._repo, "log_quota_event", new_callable=AsyncMock):
            with pytest.raises(HTTPException) as exc_info:
                await svc.check_and_add_storage(1, 100)
            assert exc_info.value.status_code == 402


# ─── Tenant cache ─────────────────────────────────────────────────────────────

class TestTenantCache:
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        cache = TenantCache()
        fake = object()
        await cache.set("dps-delhi", fake)
        result = await cache.get("dps-delhi")
        assert result is fake

    @pytest.mark.asyncio
    async def test_cache_invalidate(self):
        cache = TenantCache()
        await cache.set("xyz-school", "some-tenant")
        await cache.invalidate("xyz-school")
        result = await cache.get("xyz-school")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_miss_returns_none(self):
        cache = TenantCache()
        result = await cache.get("nonexistent-slug")
        assert result is None


# ─── Subdomain extraction ─────────────────────────────────────────────────────

class TestSlugExtraction:
    @pytest.mark.parametrize("host,expected", [
        ("dps-delhi.eduforge.in", "dps-delhi"),
        ("resonance.eduforge.in", "resonance"),
        ("api.eduforge.in", None),
        ("www.eduforge.in", None),
        ("admin.eduforge.in", None),
        ("dps-delhi.edvance.in", "dps-delhi"),
        ("someother.com", None),
        ("dps-delhi.eduforge.in:8000", "dps-delhi"),  # port stripped
    ])
    def test_extract_slug(self, host, expected):
        assert _extract_slug(host) == expected


# ─── Academic year utility ────────────────────────────────────────────────────

class TestAcademicYear:
    def test_june_start_in_july(self):
        from datetime import date
        year = current_academic_year(start_month=6, ref=date(2025, 7, 15))
        assert year == "2025-26"

    def test_june_start_in_april(self):
        from datetime import date
        year = current_academic_year(start_month=6, ref=date(2025, 4, 1))
        assert year == "2024-25"

    def test_april_start(self):
        from datetime import date
        year = current_academic_year(start_month=4, ref=date(2025, 5, 1))
        assert year == "2025-26"

    def test_bounds(self):
        from datetime import date
        start, end = academic_year_bounds(start_month=6, ref=date(2025, 8, 1))
        assert start == date(2025, 6, 1)
        assert end.year == 2026
        assert end.month == 5


# ─── Branding validation ──────────────────────────────────────────────────────

class TestBrandingValidation:
    def test_valid_hex_color(self):
        from api.modules.tenancy.schemas.tenant_schema import BrandingUpdate
        obj = BrandingUpdate(primary_color="#1B4F72", secondary_color="#2E86C1")
        assert obj.primary_color == "#1B4F72"

    def test_invalid_hex_rejected(self):
        from api.modules.tenancy.schemas.tenant_schema import BrandingUpdate
        with pytest.raises(ValidationError):
            BrandingUpdate(primary_color="blue")

    def test_no_color_is_ok(self):
        from api.modules.tenancy.schemas.tenant_schema import BrandingUpdate
        obj = BrandingUpdate()  # all optional
        assert obj.primary_color is None
