from fastapi import APIRouter, HTTPException, status

from app.api.deps import DB, CurrentUser
from app.core.security import create_access_token
from app.crud.user import crud_user
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(body: LoginRequest, db: DB):
    user = await crud_user.authenticate(db, body.email, body.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token({"sub": user.email, "user_id": user.id})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user
