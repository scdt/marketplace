"""Модуль содержит класс AdvertisementStorage."""

from src.app.data_sources.dtos.advertisement import Advertisement


class AdvertisementStorage(object):
    """Класс хранилища объявлений."""

    advertisements = []

    def get_by_id(self, ad_id: int) -> Advertisement:
        """Получение объявления по id.

        Args:
            ad_id (int): id объявления

        Raises:
            ValueError: объявления с указанным id не найдено

        Returns:
            Advertisement: объявление
        """
        try:
            return self.advertisements[ad_id]
        except IndexError:
            raise ValueError('Объявления с указанным id не найдено')
    
    def get_all(self) -> list:
        """Получить все объявления.

        Returns:
            list: объявления
        """
        return self.advertisements

    def add(self, type: str, owner: str, title: str, price: int, description: str):
        """Создание нового объявлени.

        Args:
            type (str): тип объявления
            owner (str): владелец
            title (str): заголовок
            price (int): стоимость
            description (str): описание
        """
        new_id = len(self.advertisements)
        self.advertisements.append(Advertisement(
            id=new_id,
            type=type,
            owner=owner,
            title=title,
            price=price,
            description=description,
        ))
    
    def remove(self, ad_id: int):
        """Удалить объявление.

        Args:
            ad_id (int): id объявления

        Raises:
            ValueError: объявления с указанным id не найдено
        """
        try:
            self.advertisements.pop(ad_id)
        except IndexError:
            raise ValueError('Объявления с указанным id не найдено')
