from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.genres.crud import get_genre_by_id
from core.models import Genre
from utils.db_helper import db_helper


async def get_genre_by_id_dependency(
    genre_id: int, session: AsyncSession = Depends(db_helper.session_getter)
) -> Genre | HTTPException:
    if not (genre := await get_genre_by_id(genre_id=genre_id, session=session)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found."
        )
    return genre
