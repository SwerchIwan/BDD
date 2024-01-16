from http.client import HTTPException
from typing import List, Dict

from fastapi import APIRouter, Request, Query, Depends, File, UploadFile, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import pandas as pd

from src.work.router import upload_file

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="../templates")
templates_reg = Jinja2Templates(directory="../templates/auth-reg")


@router.get("/result_analysis", response_class=HTMLResponse)
def get_result_analysis_page(request: Request, file):
    df = pd.read_excel(file)
    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="File not found")

    return templates.TemplateResponse("result-analysis.html", {"request": request, "file": file, "df":df})


@router.get("/main")
def get_main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/reg")
def get_reg_page(request: Request):
    return templates_reg.TemplateResponse("registration.html", {"request": request})


@router.get("/auth")
def get_auth_page(request: Request):
    return templates_reg.TemplateResponse("auth.html", {"request": request})


@router.get("/analysis")
def get_analysis_page(request: Request):
    return templates.TemplateResponse("work.html", {"request": request})


