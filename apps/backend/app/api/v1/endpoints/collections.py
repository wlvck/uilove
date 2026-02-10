import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DB
from app.crud.collection import crud_collection
from app.crud.website import crud_website
from app.models.collection import Collection
from app.schemas.collection import CollectionRead
from app.schemas.common import PaginatedResponse
from app.schemas.website import WebsiteListItem

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("", response_model=list[CollectionRead])
async def list_collections(db: DB):
    return await crud_collection.get_multi(
        db, limit=200, filters=[Collection.is_active.is_(True)]
    )


@router.get("/{slug}/websites", response_model=PaginatedResponse[WebsiteListItem])
async def collection_websites(
    slug: str,
    db: DB,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    collection = await crud_collection.get_by_slug(db, slug)
    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    items = await crud_website.get_by_collection(
        db, collection.id, offset=(page - 1) * size, limit=size
    )
    total = await crud_website.count_by_collection(db, collection.id)
    return PaginatedResponse(
        items=items, total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 0,
    )
