from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from core.models.game import Game
    from core.models.user import User


class Review(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    ratings: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    game: Mapped["Game"] = relationship(back_populates="reviews")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="reviews")