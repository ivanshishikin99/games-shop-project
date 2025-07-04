from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey
from .base import Base

if TYPE_CHECKING:
    from core.models.game import Game
    from core.models.genre import Genre

game_genre_association_table = Table(
    "game_genre_association",
    Base.metadata,
    Column("game_id", ForeignKey("game.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)
