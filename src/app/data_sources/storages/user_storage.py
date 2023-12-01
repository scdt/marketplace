"""Модуль содержит класс UserStorage."""

from bcrypt import gensalt, hashpw
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data_sources.dtos.user import User
from src.app.data_sources.models import UserAlchemyModel


class UserStorage(object):
    """Хранилище пользователей."""

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        """Получить пользователя по id.

        Args:
            session: (AsyncSession): сессия подключения к бд
            user_id (int): id пользователя

        Returns:
            User | None: пользователь или None если пользователь не найден
        """
        user = (await session.execute(
            select(UserAlchemyModel).where(
                UserAlchemyModel.id == user_id,
            ),
        )).scalar()
        if user:
            return User.from_orm(user)

    async def get_user_by_username(self, session: AsyncSession, username: str) -> User | None:
        """Получить пользователя по имени.

        Args:
            session: (AsyncSession): сессия подключения к бд
            username (str): имя пользователя

        Returns:
            User | None: пользователь или None если пользователь не найден
        """
        user = (await session.execute(
            select(UserAlchemyModel).where(
                UserAlchemyModel.username == username,
            ),
        )).scalar()
        if user:
            return User.from_orm(user)

    async def add_user(self, session: AsyncSession, username: str, password: str):
        """Добавление нового пользователя.

        Args:
            session: (AsyncSession): сессия подключения к бд
            username (str): имя пользователя
            password (str): пароль пользователя

        Raises:
            ValueError: пользователь с таким именем уже существует
        """
        user = await self.get_user_by_username(session=session, username=username)
        if user:
            raise ValueError('Пользователь с таким именем уже существует')

        await session.execute(
            insert(UserAlchemyModel).values(
                username=username,
                password_hash=hashpw(password.encode(), gensalt()).decode(),
                is_admin=False,
            ),
        )
        await session.commit()

    async def update_user(self, session: AsyncSession, username: str, updated_user: User):
        """Изменение данных пользователя.

        Args:
            session: (AsyncSession): сессия подключения к бд
            username (str): имя пользователя
            updated_user (User): измененный пользователь

        Raises:
            ValueError: пользователя с таким именем не существует
        """
        user = await self.get_user_by_username(session=session, username=username)
        if not user:
            raise ValueError('Пользователя с таким именем не существует')

        await session.execute(
            update(UserAlchemyModel).where(
                UserAlchemyModel.id == user.user_id,
            ).values(
                username=updated_user.username,
                password_hash=updated_user.password_hash,
                is_admin=updated_user.is_admin,
            ),
        )
        await session.commit()
