import math

from fastapi import APIRouter, Query

from app.api.deps import DB
from app.crud.website import crud_website
from app.schemas.common import PaginatedResponse
from app.schemas.website import WebsiteListItem

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=PaginatedResponse[WebsiteListItem])
async def search_websites(
    db: DB,
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    items, total = await crud_website.search(
        db, q, offset=(page - 1) * size, limit=size
    )
    return PaginatedResponse(
        items=items, total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 0,
    )
