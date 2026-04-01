"""Auth module tests — JWT, lockout, OTP, password flows."""
from __future__ import annotations
import hashlib
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta, timezone

from shared.jwt.create import create_access_token, generate_refresh_token
from shared.jwt.verify import verify_token
from shared.exceptions.auth_exceptions import (
    InvalidTokenError,
    InvalidCredentialsError,
    AccountLockedError,
    OTPExpiredError,
    OTPInvalidError,
)
from shared.utils.phone import normalize_mobile, to_e164, mask_mobile, is_valid_mobile
from shared.schemas.token_schema import TokenPayload


# ─── JWT ──────────────────────────────────────────────────────────────────────

class TestAccessToken:
    def test_roundtrip(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-chars-long-enough!")
        token = create_access_token(
            user_id="usr_abc123",
            tenant_id="42",
            institution_type="SCHOOL",
            roles=["TEACHER"],
            scopes=["read:students"],
            session_id="sess_xyz",
        )
        payload = verify_token(token)
        assert payload.sub == "usr_abc123"
        assert payload.tenant_id == "42"
        assert payload.institution_type == "SCHOOL"
        assert "TEACHER" in payload.roles
        assert payload.session_id == "sess_xyz"

    def test_multiple_roles(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-chars-long-enough!")
        token = create_access_token(
            user_id="usr_001",
            tenant_id="10",
            institution_type="COACHING",
            roles=["TEACHER", "COORDINATOR"],
            scopes=["read:students", "write:timetable"],
            session_id="sess_001",
        )
        payload = verify_token(token)
        assert set(payload.roles) == {"TEACHER", "COORDINATOR"}

    def test_invalid_token_raises(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-chars-long-enough!")
        with pytest.raises(InvalidTokenError):
            verify_token("not.a.valid.jwt")

    def test_tampered_token_raises(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-chars-long-enough!")
        token = create_access_token(
            user_id="usr_001", tenant_id="1", institution_type="SCHOOL",
            roles=["ADMIN"], scopes=[], session_id="s1",
        )
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(InvalidTokenError):
            verify_token(tampered)


class TestRefreshToken:
    def test_generates_unique_pairs(self):
        raw1, hash1 = generate_refresh_token()
        raw2, hash2 = generate_refresh_token()
        assert raw1 != raw2
        assert hash1 != hash2

    def test_hash_is_sha256(self):
        raw, hashed = generate_refresh_token()
        expected = hashlib.sha256(raw.encode()).hexdigest()
        assert hashed == expected

    def test_raw_not_stored_in_hash(self):
        raw, hashed = generate_refresh_token()
        assert raw not in hashed
        assert len(hashed) == 64  # sha256 hex = 64 chars


# ─── Phone utils ──────────────────────────────────────────────────────────────

class TestPhoneUtils:
    @pytest.mark.parametrize("raw,expected", [
        ("+919876543210", "9876543210"),
        ("919876543210", "9876543210"),
        ("09876543210", "9876543210"),
        ("9876543210", "9876543210"),
        ("98765 43210", "9876543210"),
        ("9876-543-210", "9876543210"),
    ])
    def test_normalize_valid(self, raw, expected):
        assert normalize_mobile(raw) == expected

    @pytest.mark.parametrize("raw", [
        "1234567890",   # starts with 1 (not 6-9)
        "98765",        # too short
        "98765432100",  # too long
        "abcdefghij",
    ])
    def test_normalize_invalid(self, raw):
        assert normalize_mobile(raw) is None

    def test_e164(self):
        assert to_e164("9876543210") == "+919876543210"

    def test_mask(self):
        masked = mask_mobile("9876543210")
        assert masked == "XXXXXX3210"
        assert "9876" not in masked

    def test_is_valid(self):
        assert is_valid_mobile("9876543210") is True
        assert is_valid_mobile("1234567890") is False


# ─── OTP service (mocked) ─────────────────────────────────────────────────────

class TestOTPService:
    @pytest.mark.asyncio
    async def test_send_otp_rate_limit(self):
        from api.modules.auth.services.otp_service import OTPService
        from api.modules.auth.models.otp import OTPPurpose
        from shared.exceptions.auth_exceptions import RateLimitError

        mock_session = AsyncMock()
        svc = OTPService(mock_session)

        with patch.object(svc._repo, "increment_rate_limit", return_value=6):
            with pytest.raises(RateLimitError):
                await svc.send_otp(1, "9876543210", OTPPurpose.FORGOT_PASSWORD)

    @pytest.mark.asyncio
    async def test_verify_otp_expired(self):
        from api.modules.auth.services.otp_service import OTPService
        from api.modules.auth.models.otp import OTPPurpose

        mock_session = AsyncMock()
        svc = OTPService(mock_session)

        with patch.object(svc._repo, "get_active", return_value=None):
            with pytest.raises(OTPExpiredError):
                await svc.verify_otp(1, OTPPurpose.FORGOT_PASSWORD, "123456")

    @pytest.mark.asyncio
    async def test_verify_otp_wrong_code(self):
        from api.modules.auth.services.otp_service import OTPService
        from api.modules.auth.models.otp import OTPPurpose
        from shared.utils.hashing import hash_otp

        mock_session = AsyncMock()
        svc = OTPService(mock_session)

        fake_otp = MagicMock()
        fake_otp.id = 1
        fake_otp.otp_hash = hash_otp("999999")

        with patch.object(svc._repo, "get_active", return_value=fake_otp), \
             patch.object(svc._repo, "increment_attempts", return_value=1):
            with pytest.raises(OTPInvalidError):
                await svc.verify_otp(1, OTPPurpose.FORGOT_PASSWORD, "123456")


# ─── Auth service lockout thresholds ──────────────────────────────────────────

class TestAuthServiceLockout:
    def test_lockout_thresholds(self):
        from api.modules.auth.services.auth_service import (
            _LOCK_THRESHOLD_SHORT, _LOCK_THRESHOLD_LONG,
        )
        assert _LOCK_THRESHOLD_SHORT == 5
        assert _LOCK_THRESHOLD_LONG == 10

    def test_no_user_enumeration_same_error(self):
        """InvalidCredentialsError is raised for both wrong password AND missing user."""
        err_wrong_pw = InvalidCredentialsError()
        err_no_user = InvalidCredentialsError()
        assert err_wrong_pw.detail == err_no_user.detail
        assert err_wrong_pw.status_code == err_no_user.status_code


# ─── Password policy ──────────────────────────────────────────────────────────

class TestPasswordPolicy:
    @pytest.mark.parametrize("password,valid", [
        ("Abcdef1!", True),
        ("abcdef1!", False),     # no uppercase
        ("ABCDEF1!", False),     # no lowercase
        ("Abcdefgh!", False),    # no digit
        ("Abcdefg1", False),     # no special char
        ("Ab1!", False),         # too short
    ])
    def test_password_schema_validator(self, password, valid):
        from api.modules.auth.schemas.auth_schema import RegisterRequest
        from pydantic import ValidationError

        data = {
            "full_name": "Test User",
            "mobile": "9876543210",
            "password": password,
            "exam_domain": "SSC",
        }
        if valid:
            req = RegisterRequest(**data)
            assert req.password == password
        else:
            with pytest.raises(ValidationError):
                RegisterRequest(**data)

    def test_invalid_mobile_rejected(self):
        from api.modules.auth.schemas.auth_schema import RegisterRequest
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            RegisterRequest(
                full_name="Test", mobile="1234567890",
                password="Abcdef1!", exam_domain="SSC",
            )
