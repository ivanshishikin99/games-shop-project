from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.superuser.crud import super_user_create
from api_v1.superuser.schemas import SuperUserRead, SuperUserCreate
from utils.db_helper import db_helper

router = APIRouter(prefix='/superuser', tags=['Superuser'])

@router.post('/create_superuser', response_model=SuperUserRead, status_code=status.HTTP_201_CREATED)
async def create_super_user_view(user_data: SuperUserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await super_user_create(user_data=user_data, session=session)