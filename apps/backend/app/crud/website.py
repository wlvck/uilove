from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import (
    Category,
    Collection,
    Style,
    Website,
    website_categories,
    website_collections,
    website_styles,
)


class CRUDWebsite(CRUDBase[Website]):
    def _base_query(self):
        return select(Website).options(
            selectinload(Website.categories),
            selectinload(Website.styles),
            selectinload(Website.collections),
            selectinload(Website.platform),
        )

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Website | None:
        result = await db.execute(
            self._base_query().where(Website.slug == slug, Website.is_active.is_(True))
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
    ) -> list[Website]:
        stmt = self._base_query()
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(Website.created_at.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    async def count(
        self, db: AsyncSession, *, filters: list[Any] | None = None
    ) -> int:
        stmt = select(func.count(Website.id))
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_featured(
        self, db: AsyncSession, *, limit: int = 20
    ) -> list[Website]:
        return await self.get_multi(
            db,
            limit=limit,
            filters=[Website.is_featured.is_(True), Website.is_active.is_(True)],
        )

    async def get_latest(
        self, db: AsyncSession, *, limit: int = 20
    ) -> list[Website]:
        return await self.get_multi(
            db,
            limit=limit,
            filters=[Website.is_active.is_(True)],
            order_by=Website.created_at.desc(),
        )

    async def get_popular(
        self, db: AsyncSession, *, limit: int = 20
    ) -> list[Website]:
        return await self.get_multi(
            db,
            limit=limit,
            filters=[Website.is_active.is_(True)],
            order_by=Website.view_count.desc(),
        )

    async def get_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Website]:
        stmt = (
            self._base_query()
            .join(website_categories)
            .where(
                website_categories.c.category_id == category_id,
                Website.is_active.is_(True),
            )
            .order_by(Website.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    async def count_by_category(self, db: AsyncSession, category_id: int) -> int:
        stmt = (
            select(func.count(Website.id))
            .join(website_categories)
            .where(
                website_categories.c.category_id == category_id,
                Website.is_active.is_(True),
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_by_style(
        self,
        db: AsyncSession,
        style_id: int,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Website]:
        stmt = (
            self._base_query()
            .join(website_styles)
            .where(
                website_styles.c.style_id == style_id,
                Website.is_active.is_(True),
            )
            .order_by(Website.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    async def count_by_style(self, db: AsyncSession, style_id: int) -> int:
        stmt = (
            select(func.count(Website.id))
            .join(website_styles)
            .where(
                website_styles.c.style_id == style_id,
                Website.is_active.is_(True),
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_by_collection(
        self,
        db: AsyncSession,
        collection_id: int,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Website]:
        stmt = (
            self._base_query()
            .join(website_collections)
            .where(
                website_collections.c.collection_id == collection_id,
                Website.is_active.is_(True),
            )
            .order_by(Website.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    async def count_by_collection(self, db: AsyncSession, collection_id: int) -> int:
        stmt = (
            select(func.count(Website.id))
            .join(website_collections)
            .where(
                website_collections.c.collection_id == collection_id,
                Website.is_active.is_(True),
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def search(
        self,
        db: AsyncSession,
        query: str,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Website], int]:
        pattern = f"%{query}%"
        search_filter = or_(
            Website.title.ilike(pattern),
            Website.description.ilike(pattern),
        )
        filters = [search_filter, Website.is_active.is_(True)]

        items = await self.get_multi(db, offset=offset, limit=limit, filters=filters)
        total = await self.count(db, filters=filters)
        return items, total

    async def increment_view(self, db: AsyncSession, website: Website) -> None:
        website.view_count += 1
        await db.flush()

    async def create_with_relations(
        self,
        db: AsyncSession,
        *,
        category_ids: list[int] | None = None,
        style_ids: list[int] | None = None,
        collection_ids: list[int] | None = None,
        **kwargs,
    ) -> Website:
        website = Website(**kwargs)
        db.add(website)
        await db.flush()

        if category_ids:
            cats = (await db.execute(
                select(Category).where(Category.id.in_(category_ids))
            )).scalars().all()
            website.categories = list(cats)

        if style_ids:
            styles = (await db.execute(
                select(Style).where(Style.id.in_(style_ids))
            )).scalars().all()
            website.styles = list(styles)

        if collection_ids:
            cols = (await db.execute(
                select(Collection).where(Collection.id.in_(collection_ids))
            )).scalars().all()
            website.collections = list(cols)

        await db.flush()
        await db.refresh(website)
        return website

    async def update_with_relations(
        self,
        db: AsyncSession,
        website: Website,
        *,
        category_ids: list[int] | None = None,
        style_ids: list[int] | None = None,
        collection_ids: list[int] | None = None,
        **kwargs,
    ) -> Website:
        for key, value in kwargs.items():
            if value is not None:
                setattr(website, key, value)

        if category_ids is not None:
            cats = (await db.execute(
                select(Category).where(Category.id.in_(category_ids))
            )).scalars().all()
            website.categories = list(cats)

        if style_ids is not None:
            styles = (await db.execute(
                select(Style).where(Style.id.in_(style_ids))
            )).scalars().all()
            website.styles = list(styles)

        if collection_ids is not None:
            cols = (await db.execute(
                select(Collection).where(Collection.id.in_(collection_ids))
            )).scalars().all()
            website.collections = list(cols)

        await db.flush()
        await db.refresh(website)
        return website


crud_website = CRUDWebsite(Website)
