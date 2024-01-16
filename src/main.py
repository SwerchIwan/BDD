from fastapi import FastAPI
import uvicorn
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

import os

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from type_subscription.router import router as router_sub
from group.router import router as router_group
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from work.router import router as router_work
from result_analysis.router import router as router_analysis

app = FastAPI(
    title="BizMetrics"
)

app.mount("/static", StaticFiles(directory="../static"), name="static")

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

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_sub)
app.include_router(router_group)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_work)
app.include_router(router_analysis)



app.mount("/media", StaticFiles(directory="../media"), name='media')



origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
),


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


