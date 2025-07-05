import smtplib
import uuid
from email.message import EmailMessage

from core.config import settings


def send_email(recipient: str, subject: str, body: str):
    admin_email = settings.mail_config.admin_email
    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        host=settings.mail_config.hostname, port=settings.mail_config.port
    ) as server:
        server.send_message(message)


def generate_secret_verification_code():
    return uuid.uuid4()


def send_welcome_email(user_email: str, user_username: str):
    send_email(
        recipient=user_email,
        subject="Welcome to out site!",
        body=f"Dear {user_username}.\n\nWelcome to out site!",
    )
