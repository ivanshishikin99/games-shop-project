from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user
from api_v1.users.schemas import UserRead, UserCreate
from core.models import User
from utils.db_helper import db_helper

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/register_user', response_model=UserRead, response_model_exclude_none=True, status_code=status.HTTP_202_ACCEPTED)
async def register_user_view(user: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    return await create_user(user=user, session=session)
