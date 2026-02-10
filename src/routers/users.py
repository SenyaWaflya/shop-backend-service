from typing import Annotated

from fastapi import APIRouter, Path, status

from src.schemas.users import UserDto, UserResponse
from src.services.users import UsersService

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register')
async def register(user: UserDto) -> UserResponse:
    return await UsersService.create(user)


@users_router.get('/{tg_id}', summary='Get Current User')
async def get_user(
    tg_id: Annotated[str, Path(description='ID пользователя в telegram', examples=['123456789'])],
) -> UserResponse:
    return await UsersService.get_user(tg_id)


@users_router.get('/', summary='Get All Users')
async def get_users() -> list[UserResponse]:
    return await UsersService.get_users()
