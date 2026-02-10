from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, **kwargs) -> User:
        password = kwargs.pop("password")
        kwargs["hashed_password"] = get_password_hash(password)
        return await super().create(db, **kwargs)

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> User | None:
        user = await self.get_by_email(db, email)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return user


crud_user = CRUDUser(User)
