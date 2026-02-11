import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DB, AdminUser
from app.core.cache import cache_delete_pattern
from app.crud.website import crud_website
from app.models.website import Website
from app.schemas.common import PaginatedResponse
from app.schemas.website import WebsiteCreate, WebsiteListItem, WebsiteRead, WebsiteUpdate

router = APIRouter(prefix="/websites", tags=["websites"])


@router.get("", response_model=PaginatedResponse[WebsiteListItem])
async def list_websites(
    db: DB,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: str | None = None,
    style: str | None = None,
):
    filters = [Website.is_active.is_(True)]
    items = await crud_website.get_multi(
        db, offset=(page - 1) * size, limit=size, filters=filters
    )
    total = await crud_website.count(db, filters=filters)
    return PaginatedResponse(
        items=items, total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 0,
    )


@router.get("/featured", response_model=list[WebsiteListItem])
async def featured_websites(db: DB, limit: int = Query(20, ge=1, le=100)):
    return await crud_website.get_featured(db, limit=limit)


@router.get("/latest", response_model=list[WebsiteListItem])
async def latest_websites(db: DB, limit: int = Query(20, ge=1, le=100)):
    return await crud_website.get_latest(db, limit=limit)


@router.get("/popular", response_model=list[WebsiteListItem])
async def popular_websites(db: DB, limit: int = Query(20, ge=1, le=100)):
    return await crud_website.get_popular(db, limit=limit)


@router.get("/{slug}", response_model=WebsiteRead)
async def get_website(slug: str, db: DB):
    website = await crud_website.get_by_slug(db, slug)
    if website is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Website not found")
    await crud_website.increment_view(db, website)
    return website


@router.post("", response_model=WebsiteRead, status_code=status.HTTP_201_CREATED)
async def create_website(body: WebsiteCreate, db: DB, _admin: AdminUser):
    existing = await crud_website.get_by_slug(db, body.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Slug already exists"
        )
    website = await crud_website.create_with_relations(
        db,
        title=body.title,
        slug=body.slug,
        description=body.description,
        original_url=body.original_url,
        thumbnail_url=body.thumbnail_url,
        image_url=body.image_url,
        is_featured=body.is_featured,
        platform_id=body.platform_id,
        category_ids=body.category_ids,
        style_ids=body.style_ids,
        collection_ids=body.collection_ids,
    )
    await cache_delete_pattern("websites:*")
    return website


@router.put("/{slug}", response_model=WebsiteRead)
async def update_website(slug: str, body: WebsiteUpdate, db: DB, _admin: AdminUser):
    website = await crud_website.get_by_slug(db, slug, include_inactive=True)
    if website is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Website not found")
    data = body.model_dump(exclude_unset=True)
    category_ids = data.pop("category_ids", None)
    style_ids = data.pop("style_ids", None)
    collection_ids = data.pop("collection_ids", None)
    website = await crud_website.update_with_relations(
        db,
        website,
        category_ids=category_ids,
        style_ids=style_ids,
        collection_ids=collection_ids,
        **data,
    )
    await cache_delete_pattern("websites:*")
    return website


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_website(slug: str, db: DB, _admin: AdminUser):
    website = await crud_website.get_by_slug(db, slug, include_inactive=True)
    if website is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Website not found")
    await crud_website.delete(db, website)
    await cache_delete_pattern("websites:*")
