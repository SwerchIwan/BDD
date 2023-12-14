from fastapi import FastAPI
import uvicorn
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from type_subscription.router import router as router_sub
from group.router import router as router_group
from tasks.router import router as router_tasks

app = FastAPI(
    title="BizMetrics"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_sub)
app.include_router(router_group)
app.include_router(router_tasks)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

