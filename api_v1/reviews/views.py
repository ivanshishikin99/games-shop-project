from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.reviews.crud import create_review, delete_review
from api_v1.reviews.dependencies import get_review_by_id_dependency
from api_v1.reviews.schemas import ReviewRead, ReviewCreate
from core.models import User, Review
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/create_review/", response_model=ReviewRead)
async def create_review_view(
    game_id: int,
    rating: int,
    description: str,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_by_token),
) -> Review:
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email has to be verified in order for you to leave reviews.",
        )
    review = ReviewCreate(
        rating=rating, description=description, game_id=game_id, user_id=user.id
    )
    return await create_review(review=review, session=session)


@router.get("/get_review")
@cache(expire=60)
async def get_review_by_id_view(
    review_id: int, review: Review = Depends(get_review_by_id_dependency)
):
    return {
        "game": review.game.name,
        "user": review.user.username,
        "rating": review.rating,
        "description": review.description,
    }


@router.delete("/delete_review")
async def delete_review_view(
    review_id: int,
    review: Review = Depends(get_review_by_id_dependency),
    user: User = Depends(get_user_by_token),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if not user.id == review.user_id and user.role_access != "Super user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete other users' reviews.",
        )
    return await delete_review(review=review, session=session)
