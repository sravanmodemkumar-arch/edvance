"""Async SQLAlchemy pagination — offset and cursor based."""
from __future__ import annotations
import base64
import json
from typing import Any, TypeVar
from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class OffsetPage(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    has_more: bool
    total_pages: int


class CursorPage(BaseModel):
    items: list[Any]
    next_cursor: str | None
    has_more: bool


def encode_cursor(value: Any) -> str:
    return base64.b64encode(json.dumps(value).encode()).decode()


def decode_cursor(cursor: str) -> Any:
    return json.loads(base64.b64decode(cursor).decode())


async def paginate_offset(
    session: AsyncSession,
    stmt: Select,
    page: int = 1,
    page_size: int = 20,
) -> OffsetPage:
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total: int = (await session.execute(count_stmt)).scalar_one()
    rows = (
        await session.execute(stmt.offset((page - 1) * page_size).limit(page_size))
    ).scalars().all()
    total_pages = max(1, (total + page_size - 1) // page_size)
    return OffsetPage(
        items=list(rows),
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < total,
        total_pages=total_pages,
    )
