import uuid
import aiosmtplib

from email.message import EmailMessage
from core.config import settings


async def send_email(recipient: str,
                     subject: str,
                     body: str):
    admin_email = settings.mail_config.admin_email
    message = EmailMessage()
    message['From'] = admin_email
    message['To'] = recipient
    message['Subject'] = subject
    message.set_content(body)
    await aiosmtplib.send(message,
                          sender=admin_email,
                          recipients=[recipient],
                          hostname=settings.mail_config.hostname,
                          port=settings.mail_config.port)


def generate_secret_verification_code():
    return uuid.uuid4()
