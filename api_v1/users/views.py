from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user, login_user, update_user
from api_v1.users.schemas import UserRead, UserCreate, UserUpdate
from core.models import User
from utils.db_helper import db_helper
from utils.token_helpers import TokenModel, create_access_token, create_refresh_token, get_user_by_token

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/register_user', response_model=UserRead, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def register_user_view(user: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    return await create_user(user=user, session=session)

@router.post('/login', response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login_user_view(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.session_getter)) -> TokenModel:
    user = await login_user(username=form_data.username, password=form_data.password, session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenModel(access_token=access_token,
                      refresh_token=refresh_token)

@router.get('/get_user_info', response_model=UserRead, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def get_user_info_view(user: User = Depends(get_user_by_token)) -> User | HTTPException:
    return user

@router.patch('/update_user_info', response_model=UserRead, response_model_exclude_none=True, status_code=status.HTTP_202_ACCEPTED)
async def update_user_info_view(user_info: UserUpdate, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(get_user_by_token)) -> User | HTTPException:
    return await update_user(user_to_update=user, user_info=user_info, session=session)
