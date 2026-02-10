from datetime import datetime

from pydantic import BaseModel

from app.schemas.category import CategoryRead
from app.schemas.collection import CollectionRead
from app.schemas.platform import PlatformRead
from app.schemas.style import StyleRead


class WebsiteBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    original_url: str | None = None
    thumbnail_url: str | None = None
    image_url: str | None = None
    is_featured: bool = False


class WebsiteCreate(WebsiteBase):
    platform_id: int | None = None
    category_ids: list[int] = []
    style_ids: list[int] = []
    collection_ids: list[int] = []


class WebsiteUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    original_url: str | None = None
    thumbnail_url: str | None = None
    image_url: str | None = None
    platform_id: int | None = None
    is_featured: bool | None = None
    is_active: bool | None = None
    category_ids: list[int] | None = None
    style_ids: list[int] | None = None
    collection_ids: list[int] | None = None


class WebsiteRead(WebsiteBase):
    id: int
    platform: PlatformRead | None = None
    categories: list[CategoryRead] = []
    styles: list[StyleRead] = []
    collections: list[CollectionRead] = []
    is_active: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WebsiteListItem(WebsiteBase):
    id: int
    view_count: int
    created_at: datetime

    model_config = {"from_attributes": True}
