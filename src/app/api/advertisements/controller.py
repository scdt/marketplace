"""Модуль содержащий эндпоинты связанные с объявлениями."""

from annotated_types import Ge
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from typing_extensions import Annotated

from src.app.api.advertisements.models import CreateAdvertisement
from src.app.api.users.controller import get_current_user
from src.app.data_sources.dtos.advertisement import Advertisement
from src.app.data_sources.dtos.user import User
from src.app.data_sources.storages.advertisement_storage import AdvertisementStorage

router = APIRouter()
ad_storage = AdvertisementStorage()


@router.post('/api/advertisements/create')
async def create_advertisement(
    advertisement: CreateAdvertisement,
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    """Создать новое объявление.

    Args:
        advertisement (CreateAdvertisement): объявление
        current_user (Annotated[User, Depends): текущий пользователь

    Returns:
        Response: статус код 200, объявление создано
    """
    ad_storage.add(
        category=advertisement.category,
        owner=current_user.username,
        title=advertisement.title,
        price=advertisement.price,
        description=advertisement.description,
    )
    return Response(status_code=status.HTTP_200_OK)


@router.get('/api/advertisements')
async def get_advertisements() -> list:
    """Получить список всех объявлений.

    Returns:
        list: объявления
    """
    return ad_storage.get_all()


@router.get('/api/advertisements/{ad_id}')
async def get_advertisement(ad_id: Annotated[int, Ge(0)]) -> Advertisement:
    """Получить объявление по id.

    Args:
        ad_id (int): id объявления

    Raises:
        HTTPException: объявление с указанным id не найдено

    Returns:
        Advertisement: объявление
    """
    advertisement = ad_storage.get_by_id(ad_id=ad_id)
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Объявление с указанным id не найдено',
        )
    return advertisement


@router.delete('/api/advertisements/{ad_id}')
async def remove_advertisement(
    ad_id: Annotated[int, Ge(0)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    """Удаление объявления.

    Args:
        ad_id (Annotated[int, Ge): id объявления
        current_user (Annotated[User, Depends): текущий пользователь

    Raises:
        HTTPException: объявление с указанным id не найдено
        HTTPException: текущий пользователь не является владельцем объявления

    Returns:
        Response: _description_
    """
    advertisement = ad_storage.get_by_id(ad_id=ad_id)
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Объявление с указанным id не найдено',
        )
    if advertisement.owner != current_user.username and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Текущий пользователь не является владельцем объявления',
        )
    ad_storage.remove(ad_id=ad_id)
    return Response(status_code=status.HTTP_200_OK)
