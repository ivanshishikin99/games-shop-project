from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Awaitable
from fastapi import Request, Response

@dataclass
class PathCountInfo:
    count: int = 0
    status_counts: defaultdict[int: int] = field(default_factory=lambda: defaultdict(int))

class RequestsCountMiddlwareDispatch:
    def __init__(self):
        self.counted_requests = defaultdict[str, PathCountInfo](PathCountInfo)

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        path = request.url.path
        self.counted_requests[path].count += 1
        try:
            response = await call_next(request)
        except Exception:
            self.counted_requests[path].status_counts[999] += 1
            raise
        self.counted_requests[path].status_counts[response.status_code] += 1
        return response

requests_count_middleware_dispatch = RequestsCountMiddlwareDispatch()