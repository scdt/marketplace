"""Модуль содержит pydantic модели для валидации параметров запросов и возвращаемых ответов."""

from typing import Annotated, Literal

from annotated_types import Ge
from pydantic import BaseModel, Field


class CreateAdvertisement(BaseModel):
    """Модель для создания объявления."""

    category: Literal['Sell', 'Buy', 'Service']
    title: str = Field(max_length=200)  # noqa: WPS432
    price: Annotated[int, Ge(0)]
    description: str = Field(max_length=1000)
