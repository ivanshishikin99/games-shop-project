from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.genres.schemas import GenreCreate, GenreUpdate
from core.models import Genre


async def create_genre(genre: GenreCreate, session: AsyncSession) -> Genre:
    genre_created = Genre(**genre.model_dump())
    session.add(genre_created)
    await session.commit()
    await session.refresh(genre_created)
    return genre_created


async def get_genre_by_id(genre_id: int, session: AsyncSession) -> Genre | None:
    genre = await session.get(Genre, genre_id)
    return genre


async def delete_genre(genre: Genre, session: AsyncSession):
    await session.delete(genre)
    await session.commit()
    return {"Item successfully deleted."}


async def update_genre(
    genre: Genre, new_genre: GenreUpdate, session: AsyncSession
) -> Genre:
    for k, v in new_genre.model_dump().items():
        if k:
            setattr(genre, k, v)
    await session.commit()
    return genre
