"""Модуль содержит класс AdvertisementStorage."""

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.data_sources.dtos.advertisement import Advertisement
from src.app.data_sources.models import AdvertisementAlchemyModel


class AdvertisementStorage(object):
    """Класс хранилища объявлений."""

    async def get_by_id(self, session: AsyncSession, ad_id: int) -> Advertisement | None:
        """Получение объявления по id.

        Args:
            session: (AsyncSession): сессия подключения к бд
            ad_id (int): id объявления

        Returns:
            Advertisement | None: объявление или None если не найдено
        """
        advertisement = (await session.execute(
            select(AdvertisementAlchemyModel).where(
                AdvertisementAlchemyModel.id == ad_id,
            ).options(
                selectinload(AdvertisementAlchemyModel.owner),
            ),
        )).scalar()
        if advertisement:
            return Advertisement.from_orm(advertisement)

    async def get_all(self, session: AsyncSession) -> list:
        """Получить все объявления.

        Args:
            session: (AsyncSession): сессия подключения к бд

        Returns:
            list: объявления
        """
        advertisements = (await session.execute(
            select(AdvertisementAlchemyModel).options(
                selectinload(AdvertisementAlchemyModel.owner),
            ),
        )).scalars().all()
        return [Advertisement.from_orm(ad) for ad in advertisements]

    async def add(
        self,
        session: AsyncSession,
        category: str,
        owner_id: int,
        title: str,
        price: int,
        description: str,
    ):
        """Создание нового объявлени.

        Args:
            session: (AsyncSession): сессия подключения к бд
            category (str): категория объявления
            owner_id (int): id владельца
            title (str): заголовок
            price (int): стоимость
            description (str): описание
        """
        await session.execute(
            insert(AdvertisementAlchemyModel).values(
                category=category,
                owner_id=owner_id,
                title=title,
                price=price,
                description=description,
            ),
        )
        await session.commit()

    async def remove(self, session: AsyncSession, ad_id: int):
        """Удалить объявление.

        Args:
            session: (AsyncSession): сессия подключения к бд
            ad_id (int): id объявления

        Raises:
            ValueError: объявление с указанным id не найдено
        """
        advertisement = await self.get_by_id(session=session, ad_id=ad_id)
        if not advertisement:
            raise ValueError('Объявление с указанным id не найдено')

        await session.execute(
            delete(AdvertisementAlchemyModel).where(
                AdvertisementAlchemyModel.id == advertisement.id,
            ),
        )
        await session.commit()
