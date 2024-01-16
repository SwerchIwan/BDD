import json
from io import BytesIO
import tempfile

from fastapi import APIRouter, Depends, FastAPI, UploadFile, File
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, JSONResponse
import os


from src.database import get_async_session
from src.auth.model import user

import pandas as pd


router = APIRouter(
    prefix="/work",
    tags=["Work"]
)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        data = await file.read()

        # Путь к директории сохранения файлов (в данном примере в /uploads)
        upload_directory = "uploads"

        # Если директория не существует, создаем её
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Сохранение файла на сервере
        filename = os.path.join(upload_directory, file.filename)
        with open(filename, "wb") as f:
            f.write(data)

        print(1)
        # Вернуть имя сохраненного файла для дальнейшей обработки
        return JSONResponse(content={"file_name": filename})
    except Exception as e:
        import traceback
        traceback.print_exc()  # Добавляем вывод трассировки стека
        return JSONResponse(content={"error": "Ошибка при загрузке файла"}, status_code=500)


@router.get("/analysis")
async def analysis(session: AsyncSession = Depends(get_async_session)):
    pass


