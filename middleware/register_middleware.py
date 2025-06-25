from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from .requests_count_middleware import requests_count_middleware_dispatch
from .process_time_middleware import process_time_header_middleware_dispatch
from .logging_middleware import logging_middleware_dispatch


def register_middleware(app: FastAPI):
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_methods=['*'],
                       allow_headers=['*'])

    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=process_time_header_middleware_dispatch)

    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=requests_count_middleware_dispatch)

    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=logging_middleware_dispatch)


