"""Session (refresh token) data access."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.auth.models.session import Session, PasswordResetToken


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(self, **kwargs) -> Session:
        sess = Session(**kwargs)
        self._s.add(sess)
        await self._s.flush()
        return sess

    async def get_by_token_hash(self, token_hash: str) -> Session | None:
        result = await self._s.execute(
            select(Session).where(
                Session.refresh_token_hash == token_hash,
                Session.revoked.is_(False),
                Session.expires_at > datetime.now(timezone.utc),
            )
        )
        return result.scalar_one_or_none()

    async def revoke(self, session_id: int) -> None:
        await self._s.execute(
            update(Session).where(Session.id == session_id).values(revoked=True)
        )
        await self._s.flush()

    async def revoke_family(self, family_id: str) -> None:
        """Revoke all sessions in a token family (theft detected)."""
        await self._s.execute(
            update(Session).where(Session.family_id == family_id).values(revoked=True)
        )
        await self._s.flush()

    async def revoke_all_for_user(self, user_id: int) -> None:
        await self._s.execute(
            update(Session).where(Session.user_id == user_id).values(revoked=True)
        )
        await self._s.flush()

    async def revoke_all_for_tenant(self, user_id: int, tenant_id: int) -> None:
        await self._s.execute(
            update(Session).where(
                Session.user_id == user_id,
                Session.tenant_id == tenant_id,
            ).values(revoked=True)
        )
        await self._s.flush()

    # --- Password reset tokens ---

    async def create_reset_token(self, **kwargs) -> PasswordResetToken:
        token = PasswordResetToken(**kwargs)
        self._s.add(token)
        await self._s.flush()
        return token

    async def get_reset_token(self, token_hash: str) -> PasswordResetToken | None:
        result = await self._s.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash,
                PasswordResetToken.used.is_(False),
                PasswordResetToken.expires_at > datetime.now(timezone.utc),
            )
        )
        return result.scalar_one_or_none()

    async def mark_reset_token_used(self, token_id: int) -> None:
        await self._s.execute(
            update(PasswordResetToken)
            .where(PasswordResetToken.id == token_id)
            .values(used=True)
        )
        await self._s.flush()
