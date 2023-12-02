"""Модуль содержит датакласс Advertisement."""

from dataclasses import dataclass

from src.app.data_sources.dtos.user import User
from src.app.data_sources.models import AdvertisementAlchemyModel


@dataclass
class Advertisement(object):
    """Класс объявления."""

    id: int
    category: str
    title: str
    price: int
    description: str
    owner: User

    @classmethod
    def from_orm(cls, advertisement: AdvertisementAlchemyModel):
        """Метод инициализации объявления на данных из бд.

        Args:
            advertisement (AdvertisementAlchemyModel): запись объявления из бд

        Returns:
            advertisement: объявление
        """
        return cls(
            id=advertisement.id,
            category=advertisement.category,
            title=advertisement.title,
            price=advertisement.price,
            description=advertisement.description,
            owner=User.from_orm(advertisement.owner),
        )
