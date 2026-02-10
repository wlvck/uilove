from fastapi import APIRouter

from app.api.deps import DB
from app.models.platform import Platform
from app.schemas.platform import PlatformRead

router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.get("", response_model=list[PlatformRead])
async def list_platforms(db: DB):
    from app.crud.platform import crud_platform

    return await crud_platform.get_multi(
        db, limit=200, filters=[Platform.is_active.is_(True)]
    )
