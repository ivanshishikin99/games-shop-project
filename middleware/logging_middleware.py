import logging
import time
from typing import Callable, Awaitable

from fastapi import FastAPI, Response
from fastapi.requests import Request

from core.config import settings

logging.basicConfig(level=settings.logging_config.log_level,
                    format=settings.logging_config.log_format)

log = logging.getLogger(__name__)


def register_middleware(app: FastAPI):
    logger = logging.getLogger("uvicorn.access")
    logger.disabled = True
    @app.middleware("http")
    async def custom_logging(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        now = time.perf_counter()
        result = await call_next(request)
        log.info("Request %s to %s took %s seconds.", request.method, request.url, time.perf_counter() - now)
        return result
