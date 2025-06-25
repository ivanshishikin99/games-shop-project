from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin
from core.models.game_genre import game_genre_association_table

if TYPE_CHECKING:
    from core.models.genre import Genre
    from core.models.review import Review

class Game(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    date_of_release: Mapped[date] = mapped_column(nullable=False)
    age_censor: Mapped[int] = mapped_column(nullable=False)
    developer: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[str] = mapped_column(nullable=False)
    reviews: Mapped[list["Review"]] = relationship(back_populates="game")
    genres: Mapped[list["Genre"]] = relationship(secondary=game_genre_association_table,
                                                 back_populates="games",
                                                 lazy="selectin")

