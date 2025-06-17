from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.superuser.schemas import SuperUserCreate
from core.models import User
from utils.password_helpers import hash_password, verify_password


async def super_user_create(user_data: SuperUserCreate,
                            session: AsyncSession) -> User:
    user_data.password = hash_password(password=user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def super_user_login(username: str,
                           password: str,
                           session: AsyncSession) -> User | HTTPException:
    statement = select(User).where(User.username == username)
    user = await session.execute(statement)
    user = user.scalar_one()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found.')
    if not verify_password(password=password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Wrong password.')
    return user
