from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from core.models.mixins import IdIntPkMixin
from . import Base
from core.models.game_genre import game_genre_association_table

if TYPE_CHECKING:
    from core.models.game import Game


class Genre(Base, IdIntPkMixin):
    genre_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    games: Mapped[list["Game"]] = relationship(
        secondary=game_genre_association_table, back_populates="genres", lazy="selectin"
    )
