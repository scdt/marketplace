"""Модуль содержит датакласс User."""
from dataclasses import dataclass

from src.app.data_sources.models import UserAlchemyModel


@dataclass
class User(object):
    """Класс пользователя."""

    user_id: int
    username: str
    password_hash: str
    is_admin: bool

    @classmethod
    def from_orm(cls, user: UserAlchemyModel):
        """Метод инициализации пользователя на данных из бд.

        Args:
            user (UserAlchemyModel): запись пользователя из бд

        Returns:
            User: пользователь
        """
        return cls(
            user_id=user.id,
            username=user.username,
            password_hash=user.password_hash,
            is_admin=user.is_admin,
        )
