from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.genres.crud import create_genre, update_genre, delete_genre
from api_v1.genres.dependencies import get_genre_by_id_dependency
from api_v1.genres.schemas import GenreCreate, GenreRead, GenreUpdate
from core.models import User, Genre
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix='/genres', tags=['Genres'])


@router.post('/create_genre', response_model=GenreRead, response_model_exclude_none=True)
async def create_genre_view(genre: GenreCreate,
                       session: AsyncSession = Depends(db_helper.session_getter),
                       user: User = Depends(get_user_by_token)) -> Genre:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized to view this page.')
    return await create_genre(genre=genre,
                              session=session)


@router.get('/get_genre_by_id', response_model=GenreRead, response_model_exclude_none=True)
async def get_genre_by_id_view(genre_id: int,
                               genre: Genre = Depends(get_genre_by_id_dependency)) -> Genre:
    return genre

@router.patch('/update_genre', response_model=GenreRead, response_model_exclude_none=True)
async def update_genre_view(genre_id: int,
                            genre_new: GenreUpdate,
                            session: AsyncSession = Depends(db_helper.session_getter),
                            genre: Genre = Depends(get_genre_by_id_dependency)) -> Genre:
    return await update_genre(genre=genre, new_genre=genre_new, session=session)

@router.delete('/delete_genre')
async def delete_genre_view(genre_id: int,
                            genre: Genre = Depends(get_genre_by_id_dependency),
                            session: AsyncSession = Depends(db_helper.session_getter)):
    return await delete_genre(genre=genre, session=session)

