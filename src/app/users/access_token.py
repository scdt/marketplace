"""Модуль отвечающий за создание jwt токена."""

from datetime import datetime, timedelta

from jose import jwt

from src.config.config import settings


def create_access_token(user_id: int) -> str:
    """Функция для создания jwt токена.

    Args:
        user_id (int): id пользователя

    Returns:
        str: jwt токен
    """
    expire = datetime.utcnow() + timedelta(days=settings.access_token.expire_days)
    to_encode = {
        'sub': str(user_id),
        'exp': expire,
    }
    return jwt.encode(
        to_encode,
        settings.access_token.secret,
        algorithm='HS256',
    )
