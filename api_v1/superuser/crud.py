from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.superuser.schemas import SuperUserCreate
from core.models import SuperUser
from utils.password_helpers import hash_password


async def super_user_create(user_data: SuperUserCreate, session: AsyncSession) -> SuperUser:
    user_data.password = hash_password(password=user_data.password)
    user = SuperUser(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

