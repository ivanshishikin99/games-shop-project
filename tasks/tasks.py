from logger import log
from mailing.email_helper import send_welcome_email as send
from tasks.celery import celery


@celery.task
def send_welcome_email(user_id: int,
                       user_email: str,
                       user_username: str):
    log.info("Sending welcome email to user %s", user_id)
    return send(user_email=user_email,
                user_username=user_username)