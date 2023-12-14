import smtplib
from email.message import EmailMessage

from celery import Celery

from config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'BizMetrics'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {username} 😎😎😎!</h1> '
        '<p> Благодарим вас за регистрацию на нашем сайте!! С уважением команда BizMetrics</p>'
        '</div>',
        subtype='html'
    )

    return email


def get_welcome_message(username: str, email_: str):
    email = EmailMessage()
    email['Subject'] = 'BizMetrics '
    email['From'] = SMTP_USER
    email['To'] = email_

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {username} 😎😎😎!</h1> '
        '<img src="https://opis-cdn.tinkoffjournal.ru/mercury/american-psycho-1234.1dai5n..gif" width="600">'
        '</div>',
        subtype='html'
    )

    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_welcome_message(username: str, email_: str):
    email = get_welcome_message(username, email_)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)