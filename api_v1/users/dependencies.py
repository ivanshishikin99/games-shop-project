from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import get_user_by_id
from core.models import User
from utils.db_helper import db_helper


async def get_user_by_id_dependency(
    user_id: int, session: AsyncSession = Depends(db_helper.session_getter)
) -> User | HTTPException:
    user = await get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user
