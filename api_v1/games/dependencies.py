from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.games.crud import get_game_by_id
from core.models import Game
from utils.db_helper import db_helper


async def get_game_by_id_dependency(game_id: int,
                                    session: AsyncSession = Depends(db_helper.session_getter)) -> Game | HTTPException:
    game = await get_game_by_id(game_id=game_id,
                                session=session)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return game
