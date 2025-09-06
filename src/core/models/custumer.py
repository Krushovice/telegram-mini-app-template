from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from core.mixins import UUIDMixin, TimestampMixin


class Customer(UUIDMixin, TimestampMixin, Base):

    tg_id: Mapped[int] = mapped_column(index=True, unique=True)
    username: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str | None] = mapped_column(String(64))
    phone: Mapped[str | None] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(120))
