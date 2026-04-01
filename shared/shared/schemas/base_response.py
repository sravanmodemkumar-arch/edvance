"""Standard API response envelope — used by all FastAPI services."""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "OK"
    data: T


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
