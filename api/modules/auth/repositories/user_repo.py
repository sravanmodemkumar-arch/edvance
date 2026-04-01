"""User and UserTenant data access."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.auth.models.user import User, UserTenant, UserStatus


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_uid(self, uid: str) -> User | None:
        result = await self._s.execute(
            select(User).where(User.uid == uid, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._s.execute(
            select(User).where(User.email == email, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_mobile(self, mobile: str) -> User | None:
        result = await self._s.execute(
            select(User).where(User.mobile == mobile, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_tenant_membership(
        self, user_id: int, tenant_id: int
    ) -> UserTenant | None:
        result = await self._s.execute(
            select(UserTenant).where(
                UserTenant.user_id == user_id,
                UserTenant.tenant_id == tenant_id,
                UserTenant.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def increment_failed_attempts(self, user_id: int) -> int:
        result = await self._s.execute(
            update(User)
            .where(User.id == user_id)
            .values(failed_attempts=User.failed_attempts + 1)
            .returning(User.failed_attempts)
        )
        await self._s.flush()
        return result.scalar_one()

    async def lock_account(self, user_id: int, until: datetime) -> None:
        await self._s.execute(
            update(User).where(User.id == user_id).values(locked_until=until)
        )
        await self._s.flush()

    async def reset_failed_attempts(self, user_id: int) -> None:
        await self._s.execute(
            update(User).where(User.id == user_id).values(
                failed_attempts=0,
                locked_until=None,
                last_login_at=datetime.now(timezone.utc),
            )
        )
        await self._s.flush()

    async def update_password(self, user_id: int, password_hash: str) -> None:
        await self._s.execute(
            update(User).where(User.id == user_id).values(password_hash=password_hash)
        )
        await self._s.flush()

    async def update_mobile(self, user_id: int, mobile: str) -> None:
        await self._s.execute(
            update(User).where(User.id == user_id).values(mobile=mobile)
        )
        await self._s.flush()

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self._s.add(user)
        await self._s.flush()
        return user
