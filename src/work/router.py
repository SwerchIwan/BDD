import json
from io import BytesIO
import tempfile

from fastapi import APIRouter, Depends, FastAPI, UploadFile, File
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse


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

        data_io = BytesIO(data)
        df = pd.read_excel(data_io)
        df = df.fillna('')
        print(df)

        return df
    except Exception as e:
        return RedirectResponse(url="/pages/error", status_code=302)

@router.get("/analysis")
async def analysis(session: AsyncSession = Depends(get_async_session)):
    pass


