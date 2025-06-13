import uuid
from email.message import EmailMessage

import aiosmtplib

from api_v1.users import crud
from core.models import User
from utils.db_helper import db_helper


async def send_email(recipient: str,
                     subject: str,
                     body: str):
    admin_email = 'games_shop@mail.ru'
    message = EmailMessage()
    message['From'] = admin_email
    message['To'] = recipient
    message['Subject'] = subject
    message.set_content(body)
    await aiosmtplib.send(message,
                          sender=admin_email,
                          recipients=[recipient],
                          hostname='localhost',
                          port=1025)


def generate_secret_verification_code():
    return uuid.uuid4()

async def send_email_dependency(user_id: int, secret_code: str):
    async with db_helper.session_maker() as session:
        user: User = await crud.get_user_by_id(user_id=user_id, session=session)
    await send_email(recipient=user.email,
                     subject='Email verification',
                     body=f"Your verification code is {secret_code}. If this e-mail was sent by mistake just ignore it.")