from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from core.models import Game
    from core.models import OrderGameAssociation


class Order(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    games: Mapped[list["Game"]] = relationship(secondary="order_game_association", back_populates="games")

    games_details: Mapped[list["OrderGameAssociation"]] = relationship(back_populates="order")