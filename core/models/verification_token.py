import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import CreatedAtMixin, IdIntPkMixin


class VerificationToken(Base, IdIntPkMixin, CreatedAtMixin):
    token: Mapped[uuid.UUID]
    user_email: Mapped[str] = mapped_column(ForeignKey("user.email"))
