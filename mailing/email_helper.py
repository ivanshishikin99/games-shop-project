import uuid
import aiosmtplib

from email.message import EmailMessage

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from core.config import settings
from core.models import User
from utils.db_helper import db_helper


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


async def send_welcome_email(user_id: int):
    async with db_helper.session_maker() as session:
        user: User = await crud.get_user_by_id(user_id=user_id, session=session)
    await send_email(recipient=user.email,
                     subject='Welcome to out site!',
                     body=f"Dear {user.username}.\n\nWelcome to out site!")
