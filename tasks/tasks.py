from logger import log
from mailing.email_helper import send_welcome_email as send
from mailing.email_helper import send_email
from tasks.celery import celery


@celery.task
def send_welcome_email(user_id: int,
                       user_email: str,
                       user_username: str):
    log.info("Sending welcome email to user %s", user_id)
    return send(user_email=user_email,
                user_username=user_username)


@celery.task
def send_email_verification_code(user_email: str,
                                 secret_code: str):
    return send_email(recipient=user_email,
                      subject='Email verification',
                      body=f"Your verification code is {secret_code}. If this e-mail was sent by mistake just ignore it."
                      )