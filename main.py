from contextlib import asynccontextmanager
from api_v1.views import router as api_v1_router
import uvicorn
from fastapi import FastAPI
from utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(router=api_v1_router)

@app.get('/')
async def main_page():
    return {'Success'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)