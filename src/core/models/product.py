from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer, Boolean, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from core.mixins import UUIDMixin, TimestampMixin


class Category(UUIDMixin, TimestampMixin, Base):

    name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        index=True,
    )
    slug: Mapped[str] = mapped_column(
        String(140),
        unique=True,
        index=True,
    )
    sort: Mapped[int] = mapped_column(Integer, default=0)
    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
    )


class Product(UUIDMixin, TimestampMixin, Base):

    title: Mapped[str] = mapped_column(
        String(200),
        index=True,
    )
    slug: Mapped[str] = mapped_column(
        String(240),
        unique=True,
        index=True,
    )
    description: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    category_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    category: Mapped[Category | None] = relationship(
        back_populates="products",
    )

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductVariant(UUIDMixin, TimestampMixin, Base):

    product_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        )
    )
    product: Mapped[Product] = relationship(back_populates="variants")

    sku: Mapped[str | None] = mapped_column(
        String(64),
        index=True,
    )
    price_amount: Mapped[int] = mapped_column(Integer)  # в копейках/центах
    currency: Mapped[str] = mapped_column(
        String(3),
        default="RUB",
    )
    options: Mapped[dict | None] = mapped_column(JSONB)  # {size:"M", milk:"oat"}

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class ProductImage(UUIDMixin, TimestampMixin, Base):

    product_id: Mapped["UUID"] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        )
    )
    product: Mapped[Product] = relationship(
        back_populates="images",
    )
    url: Mapped[str] = mapped_column(String(500))
    sort: Mapped[int] = mapped_column(Integer, default=0)
