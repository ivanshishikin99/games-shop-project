from api_v1.users import crud
from core.models import User
from utils.db_helper import db_helper
from mailing.email_helper import send_email


async def send_email_background_task(user_id: int,
                                     secret_code: str):
    async with db_helper.session_maker() as session:
        user: User = await crud.get_user_by_id(user_id=user_id,
                                               session=session)
    await send_email(recipient=user.email,
                     subject='Email verification',
                     body=f"Your verification code is {secret_code}. If this e-mail was sent by mistake just ignore it.")
    