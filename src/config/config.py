"""
Модуль для конфигурации проекта.

Позволяет импортировать конфигурацию из config.yml файла.
"""

from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='EMP_', env_nested_delimiter='_')

    @classmethod
    def from_yaml(cls, config_path: str) -> '_SettingsModel':
        return cls(**yaml.safe_load(Path(config_path).read_text()))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return env_settings, init_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    host: str
    port: int


class _AccessTokenSetting(_SettingsModel):
    token_type: str
    expire_days: int
    secret: str


class _PostgresSettings(_SettingsModel):
    login: str
    password: str
    db_name: str
    host: str
    port: int

    @property
    def url(self):
        return '{0}:{1}@{2}:{3}'.format(
            self.login,
            self.password,
            self.host,
            self.port,
        )

    @property
    def uri(self):
        return 'postgresql+asyncpg://{0}/{1}'.format(self.url, self.db_name)


class Settings(_SettingsModel):
    """Настройки сервиса."""

    service: _ServiceSettings
    access_token: _AccessTokenSetting
    postgres: _PostgresSettings


settings = Settings.from_yaml('src/config/config.yml')
