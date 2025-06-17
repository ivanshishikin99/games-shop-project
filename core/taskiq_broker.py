from taskiq_aio_pika import AioPikaBroker

from core.config import settings


broker = AioPikaBroker(url=settings.task_iq_config.url)
