from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User
from utils.password_helpers import hash_password


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    user.password = hash_password(password=user.password)
    user_created = User(**user.model_dump())
    session.add(user_created)
    await session.commit()
    await session.refresh(user_created)
    return user_created
