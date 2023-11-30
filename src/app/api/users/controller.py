"""Модуль содержащий эндпоинты связанные с пользователями сервиса."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

from src.app.api.users.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth')


@router.post('/api/register')
async def register(user: User) -> Response:
    """Регистрация новых пользователей.

    Args:
        user (User): новый пользователь

    Returns:
        Response: возвращаемый ответ
    """
    return Response(status_code=status.HTTP_200_OK)


@router.post('/api/auth')
async def auth_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response:
    """Аутентификация пользователя для получения jwt.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends]):
        OAuth2 форма аутентификации

    Returns:
        Response: возвращаемый ответ
    """
    return Response(status_code=status.HTTP_200_OK)


@router.post('/api/promote-to-admin')
async def promote_to_admin(username: str) -> Response:
    """Назначения пользователя администратором.

    Args:
        username (str): имя пользователя

    Returns:
        Response: возвращаемый ответ
    """
    return Response(status_code=status.HTTP_200_OK)
