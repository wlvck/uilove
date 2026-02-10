from pydantic import BaseModel


class PlatformBase(BaseModel):
    title: str
    slug: str
    website_url: str | None = None


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: int
    website_count: int
    is_active: bool

    model_config = {"from_attributes": True}
