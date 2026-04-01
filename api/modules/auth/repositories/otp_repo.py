"""OTP and rate-limit data access."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.auth.models.otp import OTP, OTPPurpose, OTPRateLimit


class OTPRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def upsert(self, user_id: int, purpose: OTPPurpose, otp_hash: str, expires_at: datetime) -> OTP:
        """Replace any existing OTP for this (user, purpose) pair."""
        await self._s.execute(
            delete(OTP).where(OTP.user_id == user_id, OTP.purpose == purpose)
        )
        otp = OTP(user_id=user_id, purpose=purpose, otp_hash=otp_hash, expires_at=expires_at)
        self._s.add(otp)
        await self._s.flush()
        return otp

    async def get_active(self, user_id: int, purpose: OTPPurpose) -> OTP | None:
        result = await self._s.execute(
            select(OTP).where(
                OTP.user_id == user_id,
                OTP.purpose == purpose,
                OTP.verified.is_(False),
                OTP.expires_at > datetime.now(timezone.utc),
            )
        )
        return result.scalar_one_or_none()

    async def increment_attempts(self, otp_id: int) -> int:
        result = await self._s.execute(
            update(OTP)
            .where(OTP.id == otp_id)
            .values(attempts=OTP.attempts + 1)
            .returning(OTP.attempts)
        )
        await self._s.flush()
        return result.scalar_one()

    async def mark_verified(self, otp_id: int) -> None:
        await self._s.execute(
            update(OTP).where(OTP.id == otp_id).values(verified=True)
        )
        await self._s.flush()

    async def get_rate_limit(self, identifier: str, purpose: OTPPurpose, window_start: datetime) -> OTPRateLimit | None:
        result = await self._s.execute(
            select(OTPRateLimit).where(
                OTPRateLimit.identifier == identifier,
                OTPRateLimit.purpose == purpose,
                OTPRateLimit.window_start >= window_start,
            )
        )
        return result.scalar_one_or_none()

    async def increment_rate_limit(self, identifier: str, purpose: OTPPurpose, window_start: datetime) -> int:
        existing = await self.get_rate_limit(identifier, purpose, window_start)
        if existing:
            await self._s.execute(
                update(OTPRateLimit)
                .where(OTPRateLimit.id == existing.id)
                .values(count=OTPRateLimit.count + 1)
            )
            await self._s.flush()
            return existing.count + 1
        limit = OTPRateLimit(identifier=identifier, purpose=purpose, count=1, window_start=window_start)
        self._s.add(limit)
        await self._s.flush()
        return 1
