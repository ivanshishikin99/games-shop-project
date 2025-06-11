from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.games.schemas import GameCreate, GameUpdatePartial, GameUpdateFull
from core.models import Game


async def create_game(game: GameCreate, session: AsyncSession) -> Game:
    game_created = Game(**game.model_dump())
    session.add(game_created)
    await session.commit()
    await session.refresh(game_created)
    return game_created

async def get_game_by_id(game_id: int, session: AsyncSession) -> Game:
    game = await session.get(Game, game_id)
    return game

async def delete_game(game: Game, session: AsyncSession):
    await session.delete(game)
    await session.commit()
    return {'Success!'}

async def update_game_partial(game_to_update: Game, game_data: GameUpdatePartial, session: AsyncSession) -> Game:
    for k, v in game_data.model_dump().items():
        if k:
            setattr(game_to_update, k, v)
    await session.commit()
    await session.refresh(game_to_update)
    return game_to_update

async def update_game_full(game_to_update: Game, game_data: GameUpdateFull, session: AsyncSession) -> Game:
    for k, v in game_data.model_dump().items():
        setattr(game_to_update, k, v)
    await session.commit()
    await session.refresh(game_to_update)
    return game_to_update
