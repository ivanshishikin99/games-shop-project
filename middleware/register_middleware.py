from .requests_count_middleware import requests_count_middleware_dispatch
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from .process_time_middleware import process_time_header_middleware_dispatch
from .logging_middleware import logging_middleware_dispatch
from fastapi import FastAPI


ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]


def register_middleware(app: FastAPI):

    app.add_middleware(CORSMiddleware,
                       allow_origins=ALLOW_ORIGINS,
                       allow_methods=['*'],
                       allow_headers=['*'])

    app.add_middleware(BaseHTTPMiddleware, dispatch=process_time_header_middleware_dispatch)

    app.add_middleware(BaseHTTPMiddleware, dispatch=requests_count_middleware_dispatch)

    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware_dispatch)


