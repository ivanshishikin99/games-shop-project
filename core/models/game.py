from datetime import date
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin


class Game(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    date_of_release: Mapped[date] = mapped_column(nullable=False)
    age_censor: Mapped[int] = mapped_column(nullable=False)
    developer: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
