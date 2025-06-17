from fastapi import APIRouter
from middleware.requests_count_middleware import requests_count_middleware_dispatch

router = APIRouter(prefix='/service', tags=['Service'])

@router.get('/stats')
def get_requests_stats():
    return {path: {"count": stats.count, "statuses": dict(stats.status_counts)} for path, stats in requests_count_middleware_dispatch.counted_requests.items()}