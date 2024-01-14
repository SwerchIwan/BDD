import json
from io import BytesIO

from fastapi import APIRouter, Depends, FastAPI, UploadFile, File
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.model import user

import pandas as pd


router = APIRouter(
    prefix="/work",
    tags=["Work"]
)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Загрузка файла
    data = await file.read()

    # Создание DataFrame с использованием pandas
    data_io = BytesIO(data)
    df = pd.read_excel(data_io)

    # Можно выполнить различные операции с DataFrame
    # Например, получить список столбцов:
    columns = df.columns.tolist()

    # Вернуть данные или выполнить другие операции по вашему выбору
    return {"columns": columns}

@router.get("/analysis")
async def analysis(session: AsyncSession = Depends(get_async_session)):
    pass


