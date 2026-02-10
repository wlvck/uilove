from pydantic import BaseModel


class StyleBase(BaseModel):
    title: str
    slug: str


class StyleCreate(StyleBase):
    pass


class StyleRead(StyleBase):
    id: int
    website_count: int
    is_active: bool

    model_config = {"from_attributes": True}
