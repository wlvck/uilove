from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_superuser: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
