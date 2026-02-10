from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), server_onupdate=func.now())


class UserModel(BaseModel):
    __tablename__ = 'users'

    tg_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    cart: Mapped['CartModel'] = relationship(back_populates='user', uselist=False)


class ProductModel(BaseModel):
    __tablename__ = 'products'

    brand: Mapped[str] = mapped_column(index=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_path: Mapped[str] = mapped_column(unique=True)


class CartModel(BaseModel):
    __tablename__ = 'carts'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    status: Mapped[str] = mapped_column(nullable=False, default='active')

    user: Mapped['UserModel'] = relationship(back_populates='cart')
    items: Mapped[list['CartItemModel']] = relationship(back_populates='cart', cascade='all, delete-orphan')


class CartItemModel(BaseModel):
    __tablename__ = 'cart_items'

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    cart: Mapped['CartModel'] = relationship(back_populates='items')
    product: Mapped['ProductModel'] = relationship()
