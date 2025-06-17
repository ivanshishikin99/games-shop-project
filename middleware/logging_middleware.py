from typing import Callable, Awaitable

from fastapi import Request, Response

from logger import log


class LoggingMiddlewareDispatch:
    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        result = await call_next(request)
        log.info("Request %s to %s", request.method, request.url)
        return result

logging_middleware_dispatch = LoggingMiddlewareDispatch()