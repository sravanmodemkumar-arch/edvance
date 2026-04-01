"""Password management — forgot flow, change password."""
from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions.auth_exceptions import InvalidCredentialsError, InvalidTokenError
from shared.utils.hashing import hash_password, verify_password
from api.modules.auth.repositories.session_repo import SessionRepository
from api.modules.auth.repositories.user_repo import UserRepository

_RESET_TOKEN_TTL_MINUTES = 30


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class PasswordService:
    def __init__(self, session: AsyncSession) -> None:
        self._user_repo = UserRepository(session)
        self._session_repo = SessionRepository(session)

    async def issue_reset_token(self, user_id: int) -> str:
        """Issue a single-use reset token after OTP is verified. Returns raw token."""
        raw = str(uuid.uuid4())
        await self._session_repo.create_reset_token(
            user_id=user_id,
            token_hash=_hash(raw),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=_RESET_TOKEN_TTL_MINUTES),
        )
        return raw

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        token_record = await self._session_repo.get_reset_token(_hash(reset_token))
        if token_record is None:
            raise InvalidTokenError()
        await self._user_repo.update_password(
            token_record.user_id, hash_password(new_password)
        )
        await self._session_repo.mark_reset_token_used(token_record.id)
        # Revoke all active sessions for security
        await self._session_repo.revoke_all_for_user(token_record.user_id)

    async def change_password(
        self, user_id: int, current_password: str, new_password: str
    ) -> None:
        user = await self._user_repo.get_by_uid(str(user_id))
        if not user or not user.password_hash:
            raise InvalidCredentialsError()
        if not verify_password(current_password, user.password_hash):
            raise InvalidCredentialsError()
        await self._user_repo.update_password(user.id, hash_password(new_password))
