from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User
from utils.password_helpers import hash_password, verify_password


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    user.password = hash_password(password=user.password)
    user_created = User(**user.model_dump())
    session.add(user_created)
    await session.commit()
    await session.refresh(user_created)
    return user_created

async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    user = await session.get(User, user_id)
    return user

async def login_user(username: str, password: str, session: AsyncSession) -> User | HTTPException:
    statement = select(User).where(User.username == username)
    user = await session.execute(statement)
    user = user.scalar_one()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong username.')
    if not verify_password(password=password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password.')
    return user
