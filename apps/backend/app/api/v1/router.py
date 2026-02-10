from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    categories,
    collections,
    platforms,
    search,
    styles,
    websites,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(websites.router)
api_router.include_router(categories.router)
api_router.include_router(styles.router)
api_router.include_router(collections.router)
api_router.include_router(platforms.router)
api_router.include_router(search.router)
