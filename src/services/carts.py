from fastapi import HTTPException, status

from src.database.repositories.cart_items import CartItemsRepository
from src.database.repositories.carts import CartsRepository
from src.schemas.cart_items import CartItemDto, CartItemResponse
from src.schemas.carts import CartResponse
from src.services.products import ProductsService


class CartsService:
    @staticmethod
    async def add_product(user_id: int, product_id: int, quantity: int) -> CartItemResponse:
        product = await ProductsService.get_product(product_id=product_id)
        if product.quantity < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough products')

        cart_model = await CartsRepository.get(user_id=user_id)
        if cart_model is None:
            await CartsRepository.create(user_id=user_id)
            cart_model = await CartsRepository.get(user_id=user_id)
        cart = CartResponse.model_validate(cart_model)
        cart_product = next((item for item in cart.items if item.product_id == product_id), None)
        if cart_product and (product.quantity < (cart_product.quantity + quantity)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough products')

        cart_item_dto = CartItemDto(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )
        return CartItemResponse.model_validate(await CartItemsRepository.add(cart_item_dto=cart_item_dto))

    @staticmethod
    async def get_active_cart(user_id: int) -> CartResponse:
        cart_model = await CartsRepository.get(user_id=user_id)
        if cart_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart not found')
        return CartResponse.model_validate(cart_model)

    @staticmethod
    async def delete_product(user_id: int, product_id: int) -> CartItemResponse:
        cart_model = await CartsRepository.get(user_id=user_id)
        if cart_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart not found')
        cart = CartResponse.model_validate(cart_model)
        cart_item_model = await CartItemsRepository.delete(cart_id=cart.id, product_id=product_id)
        return CartItemResponse.model_validate(cart_item_model)

    @staticmethod
    async def delete_cart(user_id: int) -> CartResponse:
        cart_model = await CartsRepository.delete(user_id=user_id)
        return CartResponse.model_validate(cart_model)
