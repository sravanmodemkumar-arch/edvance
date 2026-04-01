"""OTP generation, delivery, and verification."""
from __future__ import annotations
import random
import string
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions.auth_exceptions import OTPExpiredError, OTPInvalidError, RateLimitError
from shared.utils.hashing import hash_otp, verify_otp
from api.modules.auth.models.otp import OTPPurpose
from api.modules.auth.repositories.otp_repo import OTPRepository

_OTP_LENGTH = 6
_OTP_TTL_MINUTES = 10
_MAX_PER_DAY = 5           # max OTP sends per identifier per purpose per day
_MAX_VERIFY_ATTEMPTS = 3   # wrong OTP attempts before invalidation


def _generate_otp() -> str:
    return "".join(random.choices(string.digits, k=_OTP_LENGTH))


class OTPService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = OTPRepository(session)

    async def send_otp(
        self,
        user_id: int,
        identifier: str,   # mobile or email (for delivery + rate-limiting)
        purpose: OTPPurpose,
    ) -> None:
        window_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        count = await self._repo.increment_rate_limit(identifier, purpose, window_start)
        if count > _MAX_PER_DAY:
            raise RateLimitError()

        otp = _generate_otp()
        otp_hash = hash_otp(otp)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=_OTP_TTL_MINUTES)
        await self._repo.upsert(user_id, purpose, otp_hash, expires_at)

        # Dispatch delivery — actual SMS/email via notification module
        await _dispatch_otp(identifier, otp, purpose)

    async def verify_otp(
        self,
        user_id: int,
        purpose: OTPPurpose,
        otp_plain: str,
    ) -> None:
        record = await self._repo.get_active(user_id, purpose)
        if record is None:
            raise OTPExpiredError()

        attempts = await self._repo.increment_attempts(record.id)
        if attempts > _MAX_VERIFY_ATTEMPTS:
            raise OTPInvalidError()

        if not verify_otp(otp_plain, record.otp_hash):
            raise OTPInvalidError()

        await self._repo.mark_verified(record.id)


async def _dispatch_otp(identifier: str, otp: str, purpose: OTPPurpose) -> None:
    """Fire-and-forget delivery. Production: enqueue to notification worker."""
    # Phase 1: direct Gupshup / MSG91 call
    # Phase 2+: enqueue to SQS notification queue
    # For now: log only (notification module wires this up)
    import logging
    logging.getLogger(__name__).info(
        "OTP dispatch", extra={"identifier": identifier[-4:], "purpose": purpose}
    )
