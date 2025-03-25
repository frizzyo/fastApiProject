from fastapi import APIRouter, Query, Body, HTTPException
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app.schemas.hotels import HotelPatch, HotelAdd
from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.repos.hotels import HotelsRepos
from app.exceptions import NotFound, MultipleResult

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение 1 отеля по его id")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepos(session).get_one_or_none(id=hotel_id)


@router.get("/", summary='Получение списка отелей')
async def get_hotels(
        pagination_params: PaginationDep,
        title: str | None = Query(None, description='Name of the hotel'),
        location: str | None = Query(None, description='Location of the hotel'),
):
    per_page = pagination_params.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepos(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination_params.page - 1)
        )


@router.delete("/{hotel_id}", summary='Удаление отеля')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        try:
            await HotelsRepos(session).delete(id=hotel_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {"status": "success"}


@router.post("/", summary='Добавление отеля')
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": 'Москва', "value": {
        "title": "Москва 5 звезд",
        "location": "Ул. Пушкина, д. Колотушкина",
    }},
    "2": {"summary": 'Астана', "value": {
        "title": "Астана 4 звезды",
        "location": "Астана, Ул. Пушкина, д. Колотушкина",
    }},
})):
    async with async_session_maker() as session:
        data = await HotelsRepos(session).add(hotel_data)
        await session.commit()
    return {"status": "success", "data": data}


@router.put("/{hotel_id}", summary='Изменение отеля')
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        try:
            await HotelsRepos(session).edit(hotel_data, id=hotel_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}


@router.patch("/{hotel_id}",
              summary='Частичное обновление данных об отеле',
              description='Частичное обновление какого либо значения отеля: можно отправить и name, и title')
async def update_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        try:
            await HotelsRepos(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}
