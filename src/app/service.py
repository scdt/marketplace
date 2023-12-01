"""Модуль является точкой входа в приложение."""

import uvicorn
from fastapi import FastAPI

from src.app.api.advertisements.controller import router as ad_router
from src.app.api.users.controller import router as users_router
from src.config.config import settings

app = FastAPI()
app.include_router(users_router)
app.include_router(ad_router)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.service.host,
        port=settings.service.port,
    )
