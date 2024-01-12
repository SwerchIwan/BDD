from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="../templates")
templates_reg = Jinja2Templates(directory="../templates/auth-reg")

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


