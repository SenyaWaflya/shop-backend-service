from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from src.database.connection import async_session
from src.database.models import CartItemModel, CartModel


class CartsRepository:
    @staticmethod
    async def get(user_id: int) -> CartModel | None:
        async with async_session() as session:
            query = (
                select(CartModel)
                .options(
                    selectinload(CartModel.user), selectinload(CartModel.items).selectinload(CartItemModel.product)
                )
                .where(CartModel.user_id == user_id, CartModel.status == 'active')
            )
            result = await session.execute(query)
            cart_model = result.scalar_one_or_none()
            return cart_model

    @staticmethod
    async def create(user_id: int) -> CartModel:
        async with async_session() as session:
            cart_model = CartModel(user_id=user_id, status='active')
            session.add(cart_model)
            await session.commit()
            await session.refresh(cart_model)
            return cart_model
