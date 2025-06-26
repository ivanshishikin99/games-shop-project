from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.games.dependencies import get_game_by_id_dependency
from api_v1.reviews.schemas import ReviewCreate
from api_v1.users.dependencies import get_user_by_id_dependency
from core.models import Review


async def create_review(review: ReviewCreate, session: AsyncSession) -> Review | HTTPException:
    try:
        game = await get_game_by_id_dependency(game_id=review.game_id,
                                        session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Game not found!')
    user = await get_user_by_id_dependency(user_id=review.user_id,
                                     session=session)
    review_created = Review(**review.model_dump())
    session.add(review_created)
    await session.commit()
    await session.refresh(review_created)
    statement = select(Review).where(Review.user_id==user.id, Review.game_id==game.id)
    result = await session.execute(statement)
    review = result.scalar_one()
    review.game = game
    review.user = user
    await session.commit()
    return review_created


async def get_review_by_id(review_id: int, session: AsyncSession) -> Review | None:
    return await session.get(Review, review_id)


async def delete_review(review: Review, session: AsyncSession):
    await session.delete(review)
    await session.commit()
    return {"Review successfully deleted!"}
