from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload

from src.database.connection import async_session
from src.database.models import CartItemModel
from src.schemas.cart_items import CartItemDto


class CartItemsRepository:
    @staticmethod
    async def add(cart_item_dto: CartItemDto) -> CartItemModel:
        async with async_session() as session:
            query = select(CartItemModel).where(
                CartItemModel.cart_id == cart_item_dto.cart_id, CartItemModel.product_id == cart_item_dto.product_id
            )
            result = await session.execute(query)
            cart_item_model = result.scalar_one_or_none()

            if cart_item_model is None:
                cart_item_model = CartItemModel(
                    cart_id=cart_item_dto.cart_id, product_id=cart_item_dto.product_id, quantity=cart_item_dto.quantity
                )
                session.add(cart_item_model)
                await session.commit()
                await session.refresh(cart_item_model, attribute_names=['product'])
                return cart_item_model
            cart_item_model.quantity = cart_item_model.quantity + cart_item_dto.quantity
            await session.commit()
            await session.refresh(cart_item_model, attribute_names=['product'])
            return cart_item_model

    @staticmethod
    async def delete(cart_id: int, product_id: int) -> CartItemModel:
        async with async_session() as session:
            query = select(CartItemModel).where(
                CartItemModel.cart_id == cart_id, CartItemModel.product_id == product_id
            ).options(selectinload(CartItemModel.product))
            result = await session.execute(query)
            cart_item_model = result.scalar_one()
            await session.delete(cart_item_model)
            await session.commit()
            return cart_item_model
