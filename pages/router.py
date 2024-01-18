from http.client import HTTPException
from typing import List, Dict

from fastapi_users import schemas
from fastapi import APIRouter, Request, Query, Depends, File, UploadFile, Path, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib
import base64
import seaborn as sns
from auth.base_config import current_user
from src.auth.schemas import UserCreate, UserRead
from src.auth.manager import get_user_manager, UserManager

matplotlib.use('Agg')

from src.work.router import upload_file
import src.tasks.router as elem

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="../templates")
templates_reg = Jinja2Templates(directory="../templates/auth-reg")


def generate_plots(df):
    plot_buffers = []
    # Проход по всем столбцам в DataFrame
    for column in df.columns:
        # Создание графика
        fig, ax = plt.subplots()

        # Определение типа данных столбца
        column_type = df[column].dtype
        if column_type == 'object':
            # Если столбец содержит текстовые данные, создание столбчатой диаграммы с помощью Seaborn
            sns.barplot(x=df.index, y=column, data=df, ax=ax)
        elif column_type == 'datetime64[ns]':
            # Если столбец содержит даты/время, создание линейного графика с помощью Seaborn
            sns.lineplot(x=df.index, y=column, data=df, ax=ax)
        else:
            # Для остальных числовых столбцов, создание точечной диаграммы с помощью Seaborn
            sns.scatterplot(x=df.index, y=column, data=df, ax=ax)

        # Настройки графика
        ax.set_xlabel(df.index.name)  # Подпись оси X - имя индекса DataFrame
        ax.set_ylabel(column)  # Подпись оси Y - имя столбца DataFrame

        # Преобразование графика в изображение в буфер
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Добавление буфера изображения в список
        plot_buffers.append(buffer)

        # Очистка графика для последующих итераций
        plt.close()

    return plot_buffers


@router.get("/result_analysis", response_class=HTMLResponse)
def get_result_analysis_page(request: Request, file, user=Depends(current_user)):
    df = pd.read_excel(file)
    info = df.describe().to_html()

    plot_buffers = generate_plots(df)
    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="File not found")

    plot_images = []
    for buffer in plot_buffers:
        # Преобразование буфера изображения в строку Base64
        buffer_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plot_images.append(buffer_str)
    elem.save_upload = plot_images
    return templates.TemplateResponse("result-analysis.html", {"request": request, "file": file, "df": df, "info": info, "plot_images": plot_images})


@router.get("/main")
def get_main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/reg")
def get_reg_page(request: Request):
    return templates_reg.TemplateResponse("registration.html", {"request": request})


@router.post("/reg")
async def get_reg_page(request: Request, username: str = Form(), email: str = Form(), password: str = Form(), user_manager: UserManager = Depends(get_user_manager)
):
    user_create = UserCreate(username=username, email=email, password=password, role_id=1)
    try:
        user = await user_manager.create(user_create, request=request)
        print('success')
        return {"message": "User registered successfully"}
    except Exception as e:
        print(f"Caught an exception: {e}")
        raise HTTPException(status_code=400, detail="User with this email already exists")


@router.get("/auth")
def get_auth_page(request: Request):
    return templates_reg.TemplateResponse("auth.html", {"request": request})


@router.post("/auth")
async def get_auth_page(request: Request, email: str = Form(), password: str = Form(), user_manager: UserManager = Depends(get_user_manager)):
    user_create = UserRead(email=email, password=password)
    try:
        user = await user_manager.create(user_create, request=request)
        return templates_reg.TemplateResponse("auth.html", {"request": request})
    except Exception as e:
        print(f"Caught an exception: {e}")
        raise HTTPException(status_code=400, detail="User with this email already exists")


@router.get("/analysis")
def get_analysis_page(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("work.html", {"request": request})


