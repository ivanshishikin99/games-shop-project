from fastapi import FastAPI, Request, status
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.responses import JSONResponse

from logger import log


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(request: Request, exc: ValidationError):
        log.error("Unhandled error.")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Unhandled error.", "error": exc.errors()},
        )

    @app.exception_handler(DatabaseError)
    def handle_db_error(request: Request, exc: ValidationError):
        log.error("Unhandled database error.")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Unhandled database error.", "error": exc.errors()},
        )
