from pydantic import BaseModel


class CollectionBase(BaseModel):
    title: str
    slug: str
    description: str | None = None


class CollectionCreate(CollectionBase):
    pass


class CollectionRead(CollectionBase):
    id: int
    website_count: int
    is_active: bool

    model_config = {"from_attributes": True}
