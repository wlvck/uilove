from typing import Optional

import redis.asyncio as redis

from app.core.config import settings

redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None


async def cache_get(key: str) -> Optional[str]:
    r = await get_redis()
    return await r.get(key)


async def cache_set(
    key: str, value: str, expire: int = settings.cache_expire_seconds
) -> None:
    r = await get_redis()
    await r.set(key, value, ex=expire)


async def cache_delete(key: str) -> None:
    r = await get_redis()
    await r.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    r = await get_redis()
    async for key in r.scan_iter(match=pattern):
        await r.delete(key)
