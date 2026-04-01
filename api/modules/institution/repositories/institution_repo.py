"""Institution profile data access."""
from __future__ import annotations
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.institution.models.institution import InstitutionProfile, InstitutionStatus
from api.modules.institution.models.institution_config import InstitutionConfig


class InstitutionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_tenant(self, tenant_id: int) -> InstitutionProfile | None:
        r = await self._s.execute(
            select(InstitutionProfile).where(InstitutionProfile.tenant_id == tenant_id)
        )
        return r.scalar_one_or_none()

    async def get_by_id(self, institution_id: int) -> InstitutionProfile | None:
        return await self._s.get(InstitutionProfile, institution_id)

    async def get_config(self, institution_id: int) -> InstitutionConfig | None:
        r = await self._s.execute(
            select(InstitutionConfig).where(InstitutionConfig.institution_id == institution_id)
        )
        return r.scalar_one_or_none()

    async def create(self, **kwargs) -> InstitutionProfile:
        profile = InstitutionProfile(**kwargs)
        self._s.add(profile)
        await self._s.flush()
        return profile

    async def create_config(self, **kwargs) -> InstitutionConfig:
        config = InstitutionConfig(**kwargs)
        self._s.add(config)
        await self._s.flush()
        return config

    async def update_status(self, institution_id: int, status: InstitutionStatus) -> None:
        await self._s.execute(
            update(InstitutionProfile)
            .where(InstitutionProfile.id == institution_id)
            .values(status=status)
        )
        await self._s.flush()

    async def update_profile(self, institution_id: int, **kwargs) -> None:
        await self._s.execute(
            update(InstitutionProfile)
            .where(InstitutionProfile.id == institution_id)
            .values(**kwargs)
        )
        await self._s.flush()

    async def update_config(self, institution_id: int, **kwargs) -> None:
        await self._s.execute(
            update(InstitutionConfig)
            .where(InstitutionConfig.institution_id == institution_id)
            .values(**kwargs)
        )
        await self._s.flush()
