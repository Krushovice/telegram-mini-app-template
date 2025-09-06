from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from core.mixins import UUIDMixin, TimestampMixin


class Cart(UUIDMixin, TimestampMixin, Base):

    customer_id: Mapped["UUID | None"] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    session_id: Mapped[str | None] = mapped_column(
        String(64),
        index=True,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="RUB",
    )
    subtotal_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    total_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
    )


class CartItem(UUIDMixin, TimestampMixin, Base):

    cart_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "carts.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    cart: Mapped[Cart] = relationship(
        back_populates="items",
    )

    variant_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "product_variants.id",
            ondelete="RESTRICT",
        ),
        index=True,
    )
    qty: Mapped[int] = mapped_column(Integer)
    unit_price_amount: Mapped[int] = mapped_column(Integer)
    line_amount: Mapped[int] = mapped_column(Integer)
    snapshot: Mapped[dict | None] = mapped_column(JSONB)  # снимок названия/опций
