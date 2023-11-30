"""Модуль содержит датакласс User."""
from dataclasses import dataclass


@dataclass
class User(object):
    """Класс пользователя."""

    username: str
    password_hash: str
    is_admin: bool
