from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin
from core.models import Base

if TYPE_CHECKING:
    from core.models.review import Review


class User(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    sex: Mapped[str] = mapped_column(nullable=True)
    verified: Mapped[bool] = mapped_column(nullable=False)
    role_access: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")