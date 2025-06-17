from contextlib import asynccontextmanager
from api_v1.views import router as api_v1_router
import uvicorn
from fastapi import FastAPI
from error_handlers import register_error_handlers
from middleware.register_middleware import register_middleware
from utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

app = FastAPI(lifespan=lifespan, title='Games shop')

register_error_handlers(app=app)

register_middleware(app=app)

app.include_router(router=api_v1_router)

@app.get('/')
async def main_page():
    return {'Success'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)