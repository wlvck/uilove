from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.config import settings

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(settings.default_page_size, ge=1, le=settings.max_page_size)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
