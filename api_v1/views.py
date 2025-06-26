from fastapi import APIRouter

from api_v1.users.views import router as users_router
from api_v1.games.views import router as games_router
from api_v1.superuser.views import router as superuser_router
from api_v1.genres.views import router as genres_router
from api_v1.reviews.views import router as reviews_router
from api_v1.service import router as service_router


router = APIRouter(prefix='/api_v1')

router.include_router(users_router)

router.include_router(games_router)

router.include_router(superuser_router)

router.include_router(service_router)

router.include_router(genres_router)

router.include_router(reviews_router)
