"""Модуль содержащий функции для аутентификации пользователя."""

from bcrypt import checkpw
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data_sources.dtos.user import User
from src.app.data_sources.storages.user_storage import UserStorage


async def authenticate_user(
    storage: UserStorage,
    session: AsyncSession,
    username: str,
    password: str,
) -> User:
    """Метод для проверки пароля пользователя.

    Args:
        storage (UserStorage): хранилище пользователей
        session(AsyncSession): сессия подключения к бд
        username (str): имя пользователя
        password (str): пароль пользователя

    Returns:
        User: пользователь
    """
    user = await storage.get_user_by_username(session=session, username=username)
    is_password_correct = checkpw(password.encode(), user.password_hash.encode())
    if not user or not is_password_correct:
        return False
    return user
