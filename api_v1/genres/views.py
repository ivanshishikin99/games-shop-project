from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.genres.crud import create_genre, delete_genre, update_genre
from api_v1.genres.dependencies import get_genre_by_id_dependency
from api_v1.genres.schemas import GenreCreate, GenreRead, GenreUpdate
from core.models import Genre, User
from utils.db_helper import db_helper
from utils.super_user_validation import super_user_validate
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post(
    "/create_genre", response_model=GenreRead, response_model_exclude_none=True
)
async def create_genre_view(
    genre: GenreCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_by_token),
) -> Genre:
    if super_user_validate(user=user):
        return await create_genre(genre=genre, session=session)


@router.get(
    "/get_genre_by_id", response_model=GenreRead, response_model_exclude_none=True
)
@cache(expire=60)
async def get_genre_by_id_view(
    genre_id: int,
    genre: Genre = Depends(get_genre_by_id_dependency),
    user: User = Depends(get_user_by_token),
) -> Genre:
    if super_user_validate(user=user):
        return genre


@router.get("/get_games_by_genre_id")
@cache(expire=60)
async def get_games_by_genre_id_view(
    genre_id: int,
    genre: Genre = Depends(get_genre_by_id_dependency),
    user: User = Depends(get_user_by_token),
):
    if super_user_validate(user=user):
        return genre.games


@router.patch(
    "/update_genre", response_model=GenreRead, response_model_exclude_none=True
)
async def update_genre_view(
    genre_id: int,
    genre_new: GenreUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    genre: Genre = Depends(get_genre_by_id_dependency),
    user: User = Depends(get_user_by_token),
) -> Genre:
    if super_user_validate(user=user):
        return await update_genre(genre=genre, new_genre=genre_new, session=session)


@router.delete("/delete_genre")
async def delete_genre_view(
    genre_id: int,
    genre: Genre = Depends(get_genre_by_id_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_by_token),
):
    if super_user_validate(user=user):
        return await delete_genre(genre=genre, session=session)
