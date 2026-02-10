from typing import Annotated

from pydantic import BaseModel, Field

from src.schemas.cart_items import CartItemResponse
from src.schemas.users import UserResponse


class CartResponse(BaseModel):
    id: Annotated[int, Field(description='ID корзины', ge=1)]
    user_id: Annotated[int, Field(description='ID пользователя', ge=1, examples=[1])]
    status: Annotated[str, Field(description='Статус корзины', examples=['active', 'ordered', 'abandoned'])] = 'active'
    user: Annotated[UserResponse, Field(description='Пользователь, к которому привязана корзина')]
    items: Annotated[list[CartItemResponse], Field(description='Товары данной корзины')]

    class Config:
        from_attributes = True
