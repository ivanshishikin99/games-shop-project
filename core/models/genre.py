from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.game_genre import game_genre_association_table
from core.models.mixins import IdIntPkMixin

from . import Base

if TYPE_CHECKING:
    from core.models.game import Game


class Genre(Base, IdIntPkMixin):
    genre_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    games: Mapped[list["Game"]] = relationship(
        secondary=game_genre_association_table, back_populates="genres", lazy="selectin"
    )
