"""Модуль содержит orm модель пользователя."""
from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from src.app.data_sources.models.base import Base


class UserAlchemyModel(Base):
    """Класс описывает orm модель пользователя.

    Args:
        Base (DeclarativeMeta): базовая orm модель
    """

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=100), index=True, nullable=False, unique=True)
    password_hash = Column(String(length=60), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    advertisements = relationship('AdvertisementAlchemyModel', back_populates='owner')
