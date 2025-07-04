from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.reviews.crud import get_review_by_id
from core.models import Review
from utils.db_helper import db_helper


async def get_review_by_id_dependency(
    review_id: int, session: AsyncSession = Depends(db_helper.session_getter)
) -> Review | HTTPException:
    if not (review := await get_review_by_id(review_id=review_id, session=session)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found."
        )
    return review
