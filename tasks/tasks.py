from mailing.email_helper import send_welcome_email as send
from mailing.email_helper import send_email
from tasks.celery import celery

from logger import log


@celery.task(bind=True, max_retries=5)
def send_welcome_email(self,
                       user_id: int,
                       user_email: str,
                       user_username: str):
    try:
        log.info("Sending welcome email to user with id: %s", user_id)
        return send(user_email=user_email,
                    user_username=user_username)
    except:
        self.retry()


@celery.task(bind=True, max_retries=5)
def send_email_verification_code(self,
                                 user_id: int,
                                 user_email: str,
                                 secret_code: str):
    try:
        log.info("Sending verification code to user with id: %s", user_id)
        return send_email(recipient=user_email,
                          subject='Email verification',
                          body=f"Your verification code is {secret_code}. If this e-mail was sent by mistake just ignore it."
                          )
    except:
        self.retry()