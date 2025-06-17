from fastapi import Request, Response
from typing import Callable, Awaitable
import time
class ProcessTimeHeaderMiddlewareDispatch:
    def __init__(self, name_header: str):
        self.header_name = name_header

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.perf_counter()
        result = await call_next(request)
        process_time = time.perf_counter() - start_time
        result.headers[self.header_name] = f"{process_time:.5f}"
        return result

process_time_header_middleware_dispatch = ProcessTimeHeaderMiddlewareDispatch(name_header = 'X_process_time')