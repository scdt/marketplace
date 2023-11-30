"""Модуль содержит класс UserStorage."""

from bcrypt import gensalt, hashpw

from src.app.data_sources.dtos.user import User


class UserStorage(object):
    """Хранилище пользователей."""

    users: dict = {}

    def get_user(self, username: str) -> User | None:
        """Получить пользователя по имени.

        Args:
            username (str): имя пользователя

        Returns:
            User | None: пользователь или None если пользователь не найден
        """
        return self.users.get(username)

    def add_user(self, username: str, password: str):
        """Добавление нового пользователя.

        Args:
            username (str): имя пользователя
            password (str): пароль пользователя

        Raises:
            ValueError: пользователь с таким именем уже существует
        """
        if self.users.get(username):
            raise ValueError('Пользователь с таким именем уже существует')
        self.users[username] = User(
            username=username,
            password_hash=hashpw(password.encode(), gensalt()).decode(),
            is_admin=False,
        )

    def update_user(self, username: str, updated_user: User):
        """Изменение данных пользователя.

        Args:
            username (str): имя пользователя
            updated_user (User): измененный пользователь

        Raises:
            ValueError: пользователя с таким именем не существует
        """
        if not self.users.get(username):
            raise ValueError('Пользователя с таким именем не существует')
        self.users[updated_user.username] = updated_user
        if username != updated_user.username:
            self.users.pop(username)
