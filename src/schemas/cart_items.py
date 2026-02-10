from typing import Annotated

from pydantic import BaseModel, Field

from src.schemas.products import ProductResponse


class CartItemBase(BaseModel):
    cart_id: Annotated[int, Field(description='ID корзины', ge=1, examples=[1])]
    product_id: Annotated[int, Field(description='ID товара', ge=1, examples=[1])]
    quantity: Annotated[int, Field(description='Количество товара', ge=1, examples=[1])]


class CartItemDto(CartItemBase):
    pass


class CartItemResponse(CartItemBase):
    id: Annotated[int, Field(description='ID записи о товаре в корзине', ge=1)]
    product: Annotated[ProductResponse, Field(description='Информация о товаре')]

    class Config:
        from_attributes = True
