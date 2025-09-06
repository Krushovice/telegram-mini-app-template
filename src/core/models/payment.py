from enum import Enum
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import UUIDMixin, TimestampMixin
from .base import Base

if TYPE_CHECKING:
    from core.models import Order


class PayProvider(str, Enum):
    invoice = "invoice"  # Bot Payments
    stars = "stars"  # Telegram Stars
    outer = "outer"  # внешняя реализация(через вебхук)


class PayStatus(str, Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"


class Payment(UUIDMixin, TimestampMixin, Base):

    order_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )
    order: Mapped["Order"] = relationship(
        back_populates="payment",
    )

    provider: Mapped[PayProvider] = mapped_column(
        SAEnum(
            PayProvider,
            native_enum=False,
            validate_strings=True,
            length=16,
        )
    )
    status: Mapped[PayStatus] = mapped_column(
        SAEnum(
            PayStatus,
            native_enum=False,
            validate_strings=True,
            length=16,
        ),
        default=PayStatus.pending,
    )
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(
        String(3),
        default="RUB",
    )
    provider_payload: Mapped[dict | None] = mapped_column(
        JSONB
    )  # ответ провайдера/Telegram
