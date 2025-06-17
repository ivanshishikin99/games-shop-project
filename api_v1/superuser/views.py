from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.superuser.crud import super_user_create, super_user_login
from api_v1.superuser.schemas import SuperUserRead, SuperUserCreate
from utils.db_helper import db_helper
from utils.token_helpers import create_access_token, create_refresh_token, TokenModel


router = APIRouter(prefix='/superuser', tags=['Superuser'])


@router.post('/create_superuser', response_model=SuperUserRead, status_code=status.HTTP_201_CREATED)
async def create_super_user_view(user_data: SuperUserCreate,
                                 session: AsyncSession = Depends(db_helper.session_getter)):
    return await super_user_create(user_data=user_data,
                                   session=session)


@router.post('/superuser_login', response_model=TokenModel, status_code=status.HTTP_202_ACCEPTED)
async def login_super_user_view(form_data: OAuth2PasswordRequestForm = Depends(),
                                session: AsyncSession = Depends(db_helper.session_getter)) -> TokenModel | HTTPException:
    user = await super_user_login(username=form_data.username,
                                  password=form_data.password,
                                  session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenModel(access_token=access_token,
                      refresh_token=refresh_token)
