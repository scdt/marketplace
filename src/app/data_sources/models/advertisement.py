"""Модуль содержит orm модель объявления."""
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.app.data_sources.models.base import Base


class AdvertisementAlchemyModel(Base):
    """Класс описывает orm модель объявления.

    Args:
        Base (DeclarativeMeta): базовая orm модель
    """

    __tablename__ = 'advertisements'

    id = Column(BigInteger, primary_key=True)
    category = Column(String(length=50), nullable=False)  # noqa: WPS432
    owner_id = Column(BigInteger, ForeignKey('users.id'))
    title = Column(String(length=200), nullable=False)  # noqa: WPS432
    price = Column(Integer, nullable=False)
    description = Column(String(length=1000))

    owner = relationship('UserAlchemyModel', back_populates='advertisements')
