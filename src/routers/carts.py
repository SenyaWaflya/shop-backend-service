from typing import Annotated

from fastapi import APIRouter, Body, Path

from src.schemas.cart_items import CartItemResponse
from src.schemas.carts import CartResponse
from src.services.carts import CartsService

carts_router = APIRouter(prefix='/carts', tags=['Carts'])


@carts_router.post('/{user_id}', summary='Add product to cart')
async def add_product(
    user_id: Annotated[int, Path(description='ID пользователя', examples=['1'])],
    product_id: Annotated[int, Body(description='ID товара', examples=[1])],
    quantity: Annotated[int, Body(description='Количество товара', examples=[1])],
) -> CartItemResponse:
    return await CartsService.add_product(user_id=user_id, product_id=product_id, quantity=quantity)


@carts_router.get('/{user_id}', summary='Get active cart')
async def get_cart(user_id: Annotated[int, Path(description='ID пользователя', examples=['1'])]) -> CartResponse:
    return await CartsService.get_active_cart(user_id=user_id)


@carts_router.delete('/{user_id}/{product_id}', summary='Delete item from cart')
async def delete_product(
    user_id: Annotated[int, Path(description='ID пользователя', examples=['1'])],
    product_id: Annotated[int, Path(description='ID товара, который необходимо удалить', examples=['1'])],
) -> CartItemResponse:
    return await CartsService.delete_product(user_id=user_id, product_id=product_id)


@carts_router.delete('/{user_id}', summary='Delete cart')
async def delete_cart(user_id: Annotated[int, Path(description='ID пользователя', examples=['1'])]) -> CartResponse:
    return await CartsService.delete_cart(user_id=user_id)
