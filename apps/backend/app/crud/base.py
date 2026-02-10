from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        return await db.get(self.model, id)

    async def get_by_slug(self, db: AsyncSession, slug: str) -> ModelType | None:
        result = await db.execute(
            select(self.model).where(self.model.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        offset: int = 0,
        limit: int = 20,
        filters: list[Any] | None = None,
        order_by: Any = None,
    ) -> list[ModelType]:
        stmt = select(self.model)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(self.model.id)
        stmt = stmt.offset(offset).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self, db: AsyncSession, *, filters: list[Any] | None = None
    ) -> int:
        stmt = select(func.count(self.model.id))
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        result = await db.execute(stmt)
        return result.scalar_one()

    async def create(self, db: AsyncSession, **kwargs: Any) -> ModelType:
        obj = self.model(**kwargs)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def update(
        self, db: AsyncSession, obj: ModelType, **kwargs: Any
    ) -> ModelType:
        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, obj: ModelType) -> None:
        await db.delete(obj)
        await db.flush()
