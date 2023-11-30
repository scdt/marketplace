"""Модуль содержит датакласс Advertisement."""
from dataclasses import dataclass


@dataclass
class Advertisement(object):
    """Класс объявления."""

    id: int
    type: str
    owner: str
    title: str
    price: int
    description: str
