from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    icon: str | None = None
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    website_count: int
    is_active: bool

    model_config = {"from_attributes": True}
