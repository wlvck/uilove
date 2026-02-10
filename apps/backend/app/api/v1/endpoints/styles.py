import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DB
from app.crud.style import crud_style
from app.crud.website import crud_website
from app.models.style import Style
from app.schemas.common import PaginatedResponse
from app.schemas.style import StyleRead
from app.schemas.website import WebsiteListItem

router = APIRouter(prefix="/styles", tags=["styles"])


@router.get("", response_model=list[StyleRead])
async def list_styles(db: DB):
    return await crud_style.get_multi(
        db, limit=200, filters=[Style.is_active.is_(True)]
    )


@router.get("/{slug}/websites", response_model=PaginatedResponse[WebsiteListItem])
async def style_websites(
    slug: str,
    db: DB,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    style = await crud_style.get_by_slug(db, slug)
    if style is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Style not found")
    items = await crud_website.get_by_style(
        db, style.id, offset=(page - 1) * size, limit=size
    )
    total = await crud_website.count_by_style(db, style.id)
    return PaginatedResponse(
        items=items, total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 0,
    )
