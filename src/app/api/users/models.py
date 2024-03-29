"""Модуль содержит pydantic модели для валидации параметров запросов и возвращаемых ответов."""

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    """Модель для создания пользователя."""

    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)


class AccessToken(BaseModel):
    """Модель токена доступа."""

    access_token: str
    token_type: str
