"""Core authentication service — login, logout, token refresh."""
from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions.auth_exceptions import (
    AccountDisabledError,
    AccountLockedError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from shared.jwt.create import create_access_token, generate_refresh_token
from shared.jwt.verify import verify_token
from shared.utils.hashing import verify_password
from api.modules.auth.models.user import UserStatus
from api.modules.auth.repositories.session_repo import SessionRepository
from api.modules.auth.repositories.user_repo import UserRepository
from api.modules.auth.schemas.auth_schema import LoginResponse

_REFRESH_COOKIE = "refresh_token"
_REFRESH_EXPIRE_DAYS = 7
_LOCK_THRESHOLD_SHORT = 5    # → 15 min lock
_LOCK_THRESHOLD_LONG = 10    # → 24 hr lock


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _set_refresh_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        key=_REFRESH_COOKIE,
        value=raw_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=_REFRESH_EXPIRE_DAYS * 86400,
        path="/api/v1/auth",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=_REFRESH_COOKIE, path="/api/v1/auth")


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._user_repo = UserRepository(session)
        self._session_repo = SessionRepository(session)

    async def login(
        self,
        identifier: str,
        password: str,
        tenant_slug: str,
        request: Request,
        response: Response,
    ) -> LoginResponse:
        # Resolve tenant_id from slug (cross-module call — use tenant_id integer from tenancy module)
        # For now we load it via a simple lookup. Module 02 (tenancy) will own this.
        from api.modules.tenancy.repositories import TenantRepository  # lazy import
        tenant = await TenantRepository(self._user_repo._s).get_by_slug(tenant_slug)
        if tenant is None:
            raise InvalidCredentialsError()

        # Find user — same error for not-found and wrong password (no enumeration)
        user = (
            await self._user_repo.get_by_email(identifier)
            if "@" in identifier
            else await self._user_repo.get_by_mobile(identifier.replace(" ", "").replace("-", ""))
        )
        if user is None:
            raise InvalidCredentialsError()

        # Check lockout
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            remaining_minutes = int((user.locked_until - datetime.now(timezone.utc)).total_seconds() / 60) + 1
            raise AccountLockedError(minutes=remaining_minutes)

        if user.status == UserStatus.DISABLED:
            raise AccountDisabledError()

        # Verify password
        if not user.password_hash or not verify_password(password, user.password_hash):
            attempts = await self._user_repo.increment_failed_attempts(user.id)
            if attempts >= _LOCK_THRESHOLD_LONG:
                await self._user_repo.lock_account(
                    user.id, datetime.now(timezone.utc) + timedelta(hours=24)
                )
                raise AccountLockedError(minutes=24 * 60)
            if attempts >= _LOCK_THRESHOLD_SHORT:
                await self._user_repo.lock_account(
                    user.id, datetime.now(timezone.utc) + timedelta(minutes=15)
                )
                raise AccountLockedError(minutes=15)
            raise InvalidCredentialsError()

        # Check tenant membership
        membership = await self._user_repo.get_tenant_membership(user.id, tenant.id)
        if membership is None:
            raise InvalidCredentialsError()

        # Reset failed attempts
        await self._user_repo.reset_failed_attempts(user.id)

        roles = [r.strip() for r in membership.roles.split(",") if r.strip()]
        session_uid = str(uuid.uuid4())
        raw_refresh, refresh_hash = generate_refresh_token()

        await self._session_repo.create(
            uid=session_uid,
            user_id=user.id,
            tenant_id=tenant.id,
            refresh_token_hash=refresh_hash,
            family_id=str(uuid.uuid4()),
            expires_at=datetime.now(timezone.utc) + timedelta(days=_REFRESH_EXPIRE_DAYS),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        access_token = create_access_token(
            user_id=user.uid,
            tenant_id=str(tenant.id),
            institution_type=membership.institution_type.value,
            roles=roles,
            scopes=_roles_to_scopes(roles),
            session_id=session_uid,
        )

        _set_refresh_cookie(response, raw_refresh)
        return LoginResponse(
            access_token=access_token,
            user_id=user.uid,
            full_name=user.full_name,
            roles=roles,
        )

    async def refresh(self, request: Request, response: Response) -> LoginResponse:
        raw_token = request.cookies.get(_REFRESH_COOKIE)
        if not raw_token:
            raise InvalidTokenError()

        token_hash = _hash(raw_token)
        sess = await self._session_repo.get_by_token_hash(token_hash)
        if sess is None:
            # Possible token reuse — revoke entire family if we can find it
            raise InvalidTokenError()

        # Rotate: revoke old, issue new
        await self._session_repo.revoke(sess.id)
        raw_new, hash_new = generate_refresh_token()
        session_uid = str(uuid.uuid4())
        new_sess = await self._session_repo.create(
            uid=session_uid,
            user_id=sess.user_id,
            tenant_id=sess.tenant_id,
            refresh_token_hash=hash_new,
            family_id=sess.family_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=_REFRESH_EXPIRE_DAYS),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        user = await self._user_repo.get_by_uid(str(sess.user_id))
        membership = await self._user_repo.get_tenant_membership(sess.user_id, sess.tenant_id)
        if not user or not membership:
            raise InvalidTokenError()

        roles = [r.strip() for r in membership.roles.split(",") if r.strip()]
        access_token = create_access_token(
            user_id=user.uid,
            tenant_id=str(sess.tenant_id),
            institution_type=membership.institution_type.value,
            roles=roles,
            scopes=_roles_to_scopes(roles),
            session_id=session_uid,
        )

        _set_refresh_cookie(response, raw_new)
        return LoginResponse(
            access_token=access_token,
            user_id=user.uid,
            full_name=user.full_name,
            roles=roles,
        )

    async def logout(
        self,
        request: Request,
        response: Response,
        all_devices: bool = False,
    ) -> None:
        raw_token = request.cookies.get(_REFRESH_COOKIE)
        _clear_refresh_cookie(response)
        if not raw_token:
            return
        token_hash = _hash(raw_token)
        sess = await self._session_repo.get_by_token_hash(token_hash)
        if sess:
            if all_devices:
                await self._session_repo.revoke_all_for_user(sess.user_id)
            else:
                await self._session_repo.revoke(sess.id)


def _roles_to_scopes(roles: list[str]) -> list[str]:
    """Derive permission scopes from role list."""
    scope_map: dict[str, list[str]] = {
        "STUDENT": ["read:own_profile", "read:timetable", "read:results"],
        "PARENT": ["read:child_profile", "read:child_attendance"],
        "TEACHER": ["read:students", "write:attendance", "write:homework", "read:timetable"],
        "COORDINATOR": ["read:students", "write:attendance", "write:homework",
                        "read:timetable", "write:timetable", "read:staff"],
        "ACCOUNTANT": ["read:fees", "write:fee_collection"],
        "ADMIN": ["read:*", "write:*"],
        "PLATFORM_ADMIN": ["read:*", "write:*", "platform:*"],
    }
    scopes: set[str] = set()
    for role in roles:
        scopes.update(scope_map.get(role.upper(), []))
    return sorted(scopes)
