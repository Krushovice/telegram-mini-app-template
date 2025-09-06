from enum import Enum
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from core.mixins import UUIDMixin, TimestampMixin


class OrderStatus(str, Enum):
    draft = "draft"
    awaiting_payment = "awaiting_payment"
    paid = "paid"
    fulfilled = "fulfilled"
    cancelled = "cancelled"


class DeliveryMethod(str, Enum):
    pickup = "pickup"
    delivery = "delivery"


class Order(UUIDMixin, TimestampMixin, Base):

    customer_id: Mapped["UUID | None"] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(
            OrderStatus,
            native_enum=False,
            validate_strings=True,
            length=32,
        )
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="RUB",
    )

    delivery_method: Mapped[DeliveryMethod] = mapped_column(
        SAEnum(
            DeliveryMethod,
            native_enum=False,
            validate_strings=True,
            length=32,
        )
    )
    delivery_payload: Mapped[dict | None] = mapped_column(
        JSONB
    )  # адрес/окно времени/точка самовывоза

    subtotal_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    total_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
    payment: Mapped["Payment | None"] = relationship(
        back_populates="order",
        uselist=False,
    )


class OrderItem(UUIDMixin, TimestampMixin, Base):

    order_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        )
    )
    order: Mapped[Order] = relationship(back_populates="items")

    variant_id: Mapped["UUID"]
    title: Mapped[str] = mapped_column(String(200))
    qty: Mapped[int]
    unit_price_amount: Mapped[int]
    line_amount: Mapped[int]
