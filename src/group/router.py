import json

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.model import user


router = APIRouter(
    prefix="/group",
    tags=["Grop"]
)


@router.get("/create_group")
async def create_group(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.email == email)
    result = await session.execute(query)
    # Проверяем, есть ли результаты запроса
    user_exists = result.scalar() is not None

    if user_exists:
        # Возвращаем успешный результат
        return {
            "status": "200",
            "data": None,
            "details": None,
        }
    else:
        # Возвращаем ошибку
        return {
            "status": "error",
            "data": None,
            "details": "not_valid_email"
        }
