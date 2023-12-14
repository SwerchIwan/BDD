from fastapi import APIRouter, Depends

from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard, get_welcome_message

router = APIRouter(prefix="/report")


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


