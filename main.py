import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api_v1.views import router as api_v1_router
from utils.delete_expired_verification_tokens import delete_tokens
from core.taskiq_broker import broker
from error_handlers import register_error_handlers
from middleware.register_middleware import register_middleware
from utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    asyncio.create_task(delete_tokens())
    yield
    await db_helper.dispose()
    await broker.shutdown()

app = FastAPI(lifespan=lifespan,
              title='Games shop',
              default_response_class=ORJSONResponse)

register_error_handlers(app=app)

register_middleware(app=app)

app.include_router(router=api_v1_router)

if __name__ == '__main__':
    uvicorn.run('main:app',
                reload=True)