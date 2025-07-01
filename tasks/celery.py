from celery import Celery

from core.config import settings

celery = Celery("tasks.celery",
                broker=f"{settings.celery_config.backend}://{settings.celery_config.hostname}:{settings.celery_config.port}//",
                backend='rpc://')
