import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi import Limiter
from slowapi.util import get_remote_address

from api_v1.views import router as api_v1_router
from core.config import settings
from core.taskiq_broker import broker
from error_handlers import register_error_handlers
from middleware.register_middleware import register_middleware
from utils.db_helper import db_helper
from utils.delete_expired_verification_tokens import delete_tokens

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.redis_config.hostname}:{settings.redis_config.port}"
    )
    FastAPICache.init(RedisBackend(redis), prefix=settings.redis_config.prefix)
    await broker.startup()
    asyncio.create_task(delete_tokens())
    yield
    await db_helper.dispose()
    await broker.shutdown()


app = FastAPI(
    lifespan=lifespan, title="Games shop", default_response_class=ORJSONResponse
)

limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])

app.state.limiter = limiter


register_error_handlers(app=app)

register_middleware(app=app)

app.include_router(router=api_v1_router)

@app.get('/')
async def simple_path(request: Request):
    return "Success"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
