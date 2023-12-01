"""Модуль содержит генератор для создания сессий подключения к бд."""

from asyncio import current_task

from sqlalchemy.ext import asyncio as sa_asyncio

from src.config.config import settings

engine = sa_asyncio.create_async_engine(
    url=settings.postgres.uri,
)
async_session_factory = sa_asyncio.async_sessionmaker(
    engine,
    expire_on_commit=False,
)
async_scoped_session = sa_asyncio.async_scoped_session(
    async_session_factory,
    scopefunc=current_task,
)


async def get_session() -> sa_asyncio.AsyncSession:
    """Метод для создания новой сессии подключения к бд.

    Yields:
        Iterator[AsyncSession]: новая сессия подключения к бд
    """
    session = async_scoped_session()
    try:  # noqa: WPS501
        yield session
    finally:
        await async_scoped_session.remove()
