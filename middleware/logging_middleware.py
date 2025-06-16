import logging
import time
from typing import Callable, Awaitable

from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Response
from fastapi.requests import Request

from core.config import settings

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]

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
        log.info("Request %s to %s", request.method, request.url)
        process_time = time.perf_counter() - now
        result.headers["X-Proccess-Time"] = f"{process_time:.5f}"
        return result

    app.add_middleware(CORSMiddleware,
                       allow_origins=ALLOW_ORIGINS,
                       allow_methods=['*'],
                       allow_headers=['*'])

