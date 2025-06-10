from fastapi import APIRouter
from api_v1.users.views import router as users_router

router = APIRouter(prefix='/api_v1')

router.include_router(users_router)