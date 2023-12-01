"""Модуль содержащий функции для аутентификации пользователя."""

from bcrypt import checkpw
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data_sources.storages.user_storage import UserStorage


async def authenticate_user(
    storage: UserStorage,
    session: AsyncSession,
    username: str,
    password: str,
) -> bool:
    """Метод для проверки пароля пользователя.

    Args:
        storage (UserStorage): хранилище пользователей
        session(AsyncSession): сессия подключения к бд
        username (str): имя пользователя
        password (str): пароль пользователя

    Returns:
        bool: результат проверки
    """
    user = await storage.get_user_by_username(session=session, username=username)
    if not user:
        return False
    return checkpw(password.encode(), user.password_hash.encode())
