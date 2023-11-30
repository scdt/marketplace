"""Модуль является точкой входа в приложение."""

import uvicorn
from fastapi import FastAPI

from src.config.config import settings

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.service.host,
        port=settings.service.port,
    )
