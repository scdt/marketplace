"""Модуль содержащий функции для аутентификации пользователя."""

from bcrypt import checkpw

from src.app.data_sources.storages.user_storage import UserStorage


def authenticate_user(storage: UserStorage, username: str, password: str) -> bool:
    """Метод для проверки пароля пользователя.

    Args:
        storage (UserStorage): хранилище пользователей
        username (str): имя пользователя
        password (str): пароль пользователя

    Returns:
        bool: результат проверки
    """
    user = storage.get_user(username=username)
    if not user:
        return False
    return checkpw(password.encode(), user.password_hash.encode())
