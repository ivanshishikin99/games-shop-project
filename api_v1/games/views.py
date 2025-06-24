from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.games.crud import create_game, delete_game, update_game_partial, update_game_full
from api_v1.games.dependencies import get_game_by_id_dependency
from api_v1.games.schemas import GameRead, GameCreate, GameUpdatePartial, GameUpdateFull
from core.models import Game, User
from utils.super_user_validation import super_user_validate
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token


router = APIRouter(prefix='/games', tags=['Games'])


@router.post('/create_game', response_model=GameRead, response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED)
async def create_game_view(game: GameCreate,
                           user: User = Depends(get_user_by_token),
                           session: AsyncSession = Depends(db_helper.session_getter)) -> Game | HTTPException:
    if super_user_validate(user=user):
        return await create_game(game_info=game,
                                 session=session)


@router.delete('/delete_game/{game_id}')
async def delete_game_view(game_id: int,
                           user: User = Depends(get_user_by_token),
                           game: Game = Depends(get_game_by_id_dependency),
                           session: AsyncSession = Depends(db_helper.session_getter)):
    if super_user_validate(user=user):
        return await delete_game(game=game,
                             session=session)


@router.patch('/update_game_partial', response_model=GameRead, response_model_exclude_none=True,
              status_code=status.HTTP_202_ACCEPTED)
async def update_game_partial_view(game_id: int,
                                   game_data: GameUpdatePartial,
                                   user: User = Depends(get_user_by_token),
                                   game: Game = Depends(get_game_by_id_dependency),
                                   session: AsyncSession = Depends(db_helper.session_getter)) -> Game | HTTPException:
    if super_user_validate(user=user):
        return await update_game_partial(game_to_update=game,
                                     game_data=game_data,
                                     session=session)


@router.put('/update_game_full', response_model=GameRead, response_model_exclude_none=True,
            status_code=status.HTTP_202_ACCEPTED)
async def update_game_full_view(game_id: int,
                                game_data: GameUpdateFull,
                                user: User = Depends(get_user_by_token),
                                game: Game = Depends(get_game_by_id_dependency),
                                session: AsyncSession = Depends(db_helper.session_getter)) -> Game | HTTPException:
    if super_user_validate(user=user):
        return await update_game_full(game_to_update=game,
                                  game_data=game_data,
                                  session=session)


@router.get('/get_game_info/', response_model=GameRead, response_model_exclude_none=True,
            status_code=status.HTTP_202_ACCEPTED)
async def get_game_info_by_id_view(game_id: int,
                              session: AsyncSession = Depends(db_helper.session_getter),
                              user: User = Depends(get_user_by_token),
                              game: Game = Depends(get_game_by_id_dependency)):
    if super_user_validate(user=user):
        return game


@router.get('/get_genres_by_game_id')
async def get_genres_info_by_game_id_view(game_id: int,
                                          session: AsyncSession = Depends(db_helper.session_getter),
                                          user: User = Depends(get_user_by_token),
                                          game: Game = Depends(get_game_by_id_dependency)):
    if super_user_validate(user=user):
        return game.genres
