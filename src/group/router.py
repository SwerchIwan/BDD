import json

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.model import user

from pydantic import BaseModel


router = APIRouter(
    prefix="/group",
    tags=["Grop"]
)


class GroupCreateRequest(BaseModel):
    email1: str
    email2: str
    email3: str

@router.post("/create-group")
async def create_group(request: GroupCreateRequest):
    email1 = request.email1
    email2 = request.email2
    email3 = request.email3

    print(email3)
    # Ваша логика сохранения группы
    # ...

    # Возвращаем успешный результат
    return {"status": "200", "data": None, "details": None}