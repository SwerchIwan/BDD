from fastapi import APIRouter, Depends

from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard_, get_welcome_message

from fastapi.responses import JSONResponse
from jinja2 import Template

router = APIRouter(prefix="/report")


save_upload = []


@router.get("/dashboard")
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }


@router.get("/after-reg")
def get_reg_report(user=Depends(current_user)):
    get_welcome_message.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }


@router.post("/send_email_report_dashboard")
async def send_email_report_dashboard(data: dict):
    email = data.get('username')
    print(save_upload)
    send_email_report_dashboard_(email)
    return JSONResponse(status_code=200)