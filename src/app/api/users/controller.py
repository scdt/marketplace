"""Модуль содержащий эндпоинты связанные с пользователями сервиса."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.app.api.users.models import AccessToken, CreateUser
from src.app.data_sources.adaptor import get_session
from src.app.data_sources.dtos.user import User
from src.app.data_sources.storages.user_storage import UserStorage
from src.app.users.access_token import create_access_token
from src.app.users.auth import authenticate_user
from src.config.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/auth')
user_storage = UserStorage()


async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Получение пользователя по токену доступа.

    Args:
        access_token (Annotated[str, Depends]): токен доступа
        session(AsyncSession): сессия подключения к бд

    Raises:
        HTTPException: не удалось декодировать токен
        HTTPException: пользователь с таким id не найден

    Returns:
        User: текущий пользователь
    """
    try:
        payload = jwt.decode(
            access_token,
            settings.access_token.secret,
            algorithms='HS256',
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось декодировать токен',
        )
    user_id = int(payload.get('sub'))
    if user_id:
        user = await user_storage.get_user_by_id(session=session, user_id=user_id)
        if user:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Пользователь с таким id не найден',
    )


@router.post('/api/users/register')
async def register(
    user: CreateUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Response:
    """Регистрация новых пользователей.

    Args:
        user (CreateUser): пользователь
        session(AsyncSession): сессия подключения к бд

    Raises:
        HTTPException: пользователь с таким именем уже существует

    Returns:
        Response: статус код 200, пользователь успешно создан
    """
    try:
        await user_storage.add_user(
            session=session,
            username=user.username,
            password=user.password,
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )
    return Response(status_code=status.HTTP_200_OK)


@router.post('/api/users/auth')
async def auth_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AccessToken:
    """Аутентификация пользователя для получения токена доступа.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends]):
        OAuth2 форма аутентификации
        session(AsyncSession): сессия подключения к бд

    Raises:
        HTTPException: неверрные данные пользователя

    Returns:
        AccessToken: токен доступа и тип токена
    """
    user = await authenticate_user(
        storage=user_storage,
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль или имя пользователя',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(user.user_id)
    return AccessToken(access_token=access_token, token_type=settings.access_token.token_type)


@router.post('/api/users/promote-to-admin')
async def promote_to_admin(
    username: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Response:
    """Назначения пользователя администратором.

    Args:
        username (str): имя пользователя
        current_user (Annotated[User, Depends]): текущий пользователь
        session(AsyncSession): сессия подключения к бд

    Raises:
        HTTPException: текущий пользователь не является администратором
        HTTPException: пользователь с таким именем не найден

    Returns:
        Response: статус код 200, пользователь назначен администратором
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await user_storage.get_user_by_username(session=session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем не найден',
        )
    user.is_admin = True
    await user_storage.update_user(session=session, username=username, updated_user=user)
    return Response(status_code=status.HTTP_200_OK)
