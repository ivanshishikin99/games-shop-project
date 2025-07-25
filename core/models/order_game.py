from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.game import Game


class OrderGameAssociation(Base, IdIntPkMixin):
    __table_args__ = (UniqueConstraint("order_id", "game_id"), )
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    unit_price: Mapped[int] = mapped_column(default=0, server_default="0")

    order: Mapped["Order"] = relationship(back_populates="games_details")

    game: Mapped["Game"] = relationship(back_populates="orders_details")