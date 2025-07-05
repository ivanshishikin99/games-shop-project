from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.games.schemas import GameCreate, GameUpdateFull, GameUpdatePartial
from core.models import Game, Genre


async def create_game(game_info: GameCreate, session: AsyncSession) -> Game:
    game_created = Game(
        name=game_info.name,
        price=game_info.price,
        date_of_release=game_info.date_of_release,
        age_censor=game_info.age_censor,
        developer=game_info.developer,
        rating=game_info.rating,
    )
    session.add(game_created)
    await session.commit()
    await session.refresh(game_created)
    game = await session.get(
        Game, game_created.id, options=(selectinload(Game.genres),)
    )
    for i in game_info.genres:
        try:
            statement = select(Genre).where(Genre.genre_name == i)
            genre = await session.execute(statement)
            genre = genre.scalar_one()
            game.genres.append(genre)
            await session.commit()
        except:
            genre = Genre(genre_name=i)
            session.add(genre)
            await session.commit()
            await session.refresh(genre)
            game.genres.append(genre)
            await session.commit()
    return game_created


async def get_game_by_id(game_id: int, session: AsyncSession) -> Game | None:
    game = await session.get(Game, game_id)
    return game


async def delete_game(game: Game, session: AsyncSession):
    await session.delete(game)
    await session.commit()
    return {"Success!"}


async def update_game_partial(
    game_to_update: Game, game_data: GameUpdatePartial, session: AsyncSession
) -> Game:
    if game_data.genres:
        game_to_update.genres.clear()
    for k, v in game_data.model_dump().items():
        if k and k != "genres":
            setattr(game_to_update, k, v)
        elif k == "genres":
            for i in k:
                try:
                    statement = select(Genre).where(Genre.genre_name == i)
                    genre = await session.execute(statement)
                    genre = genre.scalar_one()
                    game_to_update.genres.append(genre)
                    await session.commit()
                except:
                    genre = Genre(genre_name=i)
                    session.add(genre)
                    await session.commit()
                    await session.refresh(genre)
                    game_to_update.genres.append(genre)
                    await session.commit()
    await session.commit()
    await session.refresh(game_to_update)
    return game_to_update


async def update_game_full(
    game_to_update: Game, game_data: GameUpdateFull, session: AsyncSession
) -> Game:
    game_to_update.genres.clear()
    for k, v in game_data.model_dump().items():
        if k != "genres":
            setattr(game_to_update, k, v)
        else:
            for i in k:
                try:
                    statement = select(Genre).where(Genre.genre_name == i)
                    genre = await session.execute(statement)
                    genre = genre.scalar_one()
                    game_to_update.genres.append(genre)
                    await session.commit()
                except:
                    genre = Genre(genre_name=i)
                    session.add(genre)
                    await session.commit()
                    await session.refresh(genre)
                    game_to_update.genres.append(genre)
                    await session.commit()
    await session.commit()
    await session.refresh(game_to_update)
    return game_to_update
