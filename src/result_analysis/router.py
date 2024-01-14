import time

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database import get_async_session
router = APIRouter(prefix="/report")


router = APIRouter(
    prefix="/work_space",
    tags=["Work space"]
)


