"""ID card data access — template selection and card issuance."""
from __future__ import annotations
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.institution.models.id_card import IDCardTemplate, IDCard, CardHolderType


class IDCardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_active_template(
        self, institution_id: int, holder_type: CardHolderType
    ) -> IDCardTemplate | None:
        r = await self._s.execute(
            select(IDCardTemplate).where(
                IDCardTemplate.institution_id == institution_id,
                IDCardTemplate.holder_type == holder_type,
                IDCardTemplate.is_active.is_(True),
            ).limit(1)
        )
        return r.scalar_one_or_none()

    async def get_template(self, template_id: int) -> IDCardTemplate | None:
        return await self._s.get(IDCardTemplate, template_id)

    async def create_template(self, **kwargs) -> IDCardTemplate:
        t = IDCardTemplate(**kwargs)
        self._s.add(t)
        await self._s.flush()
        return t

    async def next_sequence(self, institution_id: int, course_code: str, year: str) -> int:
        """Atomic sequence number per (institution, course, year) tuple."""
        r = await self._s.execute(
            select(func.coalesce(func.max(IDCard.sequence_number), 0)).where(
                IDCard.institution_id == institution_id,
                IDCard.course_code == course_code,
                IDCard.academic_year == year,
            )
        )
        return (r.scalar_one() or 0) + 1

    async def create_card(self, **kwargs) -> IDCard:
        card = IDCard(**kwargs)
        self._s.add(card)
        await self._s.flush()
        return card

    async def get_card_by_number(self, id_number: str) -> IDCard | None:
        r = await self._s.execute(select(IDCard).where(IDCard.id_number == id_number))
        return r.scalar_one_or_none()

    async def get_cards_for_user(self, user_id: int) -> list[IDCard]:
        r = await self._s.execute(
            select(IDCard).where(IDCard.user_id == user_id, IDCard.is_active.is_(True))
        )
        return list(r.scalars())

    async def revoke(self, card_id: int, reason: str, now) -> None:
        await self._s.execute(
            update(IDCard).where(IDCard.id == card_id)
            .values(is_active=False, revoked_at=now, revoke_reason=reason)
        )
        await self._s.flush()
