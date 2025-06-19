import smtplib
from email.message import EmailMessage
from app.config import settings

def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = settings.SENDER_EMAIL
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
        s.login(settings.SMTP_USER, settings.SMTP_PASS)
        s.send_message(msg)
