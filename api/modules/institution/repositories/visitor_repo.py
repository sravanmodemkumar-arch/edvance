"""Visitor data access — walk-in, gate pass, QR scan."""
from __future__ import annotations
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.institution.models.visitor import Visitor, GatePassStatus


class VisitorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(self, **kwargs) -> Visitor:
        v = Visitor(**kwargs)
        self._s.add(v)
        await self._s.flush()
        return v

    async def get_by_id(self, visitor_id: int) -> Visitor | None:
        return await self._s.get(Visitor, visitor_id)

    async def get_by_qr_token(self, token: str) -> Visitor | None:
        r = await self._s.execute(select(Visitor).where(Visitor.qr_token == token))
        return r.scalar_one_or_none()

    async def list_pending(self, institution_id: int, limit: int = 50) -> list[Visitor]:
        r = await self._s.execute(
            select(Visitor).where(
                Visitor.institution_id == institution_id,
                Visitor.gate_pass_status == GatePassStatus.PENDING,
            ).order_by(Visitor.created_at.asc()).limit(limit)
        )
        return list(r.scalars())

    async def list_checked_in(self, institution_id: int) -> list[Visitor]:
        r = await self._s.execute(
            select(Visitor).where(
                Visitor.institution_id == institution_id,
                Visitor.gate_pass_status == GatePassStatus.CHECKED_IN,
            )
        )
        return list(r.scalars())

    async def update_status(
        self, visitor_id: int, status: GatePassStatus, **extra
    ) -> None:
        await self._s.execute(
            update(Visitor).where(Visitor.id == visitor_id)
            .values(gate_pass_status=status, **extra)
        )
        await self._s.flush()
