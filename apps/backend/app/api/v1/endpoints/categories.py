import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DB
from app.crud.category import crud_category
from app.crud.website import crud_website
from app.models.category import Category
from app.schemas.category import CategoryRead
from app.schemas.common import PaginatedResponse
from app.schemas.website import WebsiteListItem

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
async def list_categories(db: DB):
    return await crud_category.get_multi(
        db,
        limit=200,
        filters=[Category.is_active.is_(True)],
        order_by=Category.sort_order,
    )


@router.get("/{slug}/websites", response_model=PaginatedResponse[WebsiteListItem])
async def category_websites(
    slug: str,
    db: DB,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    category = await crud_category.get_by_slug(db, slug)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    items = await crud_website.get_by_category(
        db, category.id, offset=(page - 1) * size, limit=size
    )
    total = await crud_website.count_by_category(db, category.id)
    return PaginatedResponse(
        items=items, total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 0,
    )
