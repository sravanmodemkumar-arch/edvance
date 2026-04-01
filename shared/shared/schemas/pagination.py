"""Pagination query params — used by all list endpoints."""
from pydantic import BaseModel
from fastapi import Query


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    def total_pages(self, total: int) -> int:
        return max(1, -(-total // self.per_page))  # ceiling division


def pagination_params(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)
