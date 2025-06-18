from logger import log
from core.taskiq_broker import broker
from mailing.email_helper import send_welcome_email as send


@broker.task
async def send_welcome_email(user_id: int) -> None:
    log.info("Sending welcome email to user %s", user_id)
    await send(user_id=user_id)