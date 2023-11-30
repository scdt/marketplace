"""Модуль содержит pydantic модели для валидации параметров запросов и возвращаемых ответов."""

from pydantic import BaseModel, Field


class User(BaseModel):
    """Класс пользователя."""

    username: str = Field(max_length=100)
    password: str = Field(max_length=100)
