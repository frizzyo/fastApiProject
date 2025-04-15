from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from app.schemas.hotels import HotelPatch, HotelAdd
from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import NotFound, MultipleResult

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение 1 отеля по его id")
async def get_hotel_by_id(hotel_id: int,
                          db: DBDep):
    return await db.hotel.get_one_or_none(id=hotel_id)


@router.get("/", summary='Получение списка отелей')
async def get_hotels(
        db: DBDep,
        pagination_params: PaginationDep,
        date_from: date,
        date_to: date,
        title: str | None = Query(None, description='Name of the hotel'),
        location: str | None = Query(None, description='Location of the hotel'),
):
    per_page = pagination_params.per_page or 5
    # return await db.hotel.get_all(
    #     title=title,
    #     location=location,
    #     limit=per_page,
    #     offset=per_page * (pagination_params.page - 1)
    # )
    return await db.hotel.get_filtered_by_time(date_from=date_from,
                                               date_to=date_to,
                                               title=title,
                                               location=location,
                                               limit=per_page,
                                               offset=per_page * (pagination_params.page - 1)
                                               )


@router.delete("/{hotel_id}", summary='Удаление отеля')
async def delete_hotel(hotel_id: int,
                       db: DBDep):
    try:
        await db.hotel.delete(id=hotel_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {"status": "success"}


@router.post("/", summary='Добавление отеля')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": 'Москва', "value": {
        "title": "Москва 5 звезд",
        "location": "Ул. Пушкина, д. Колотушкина",
    }},
    "2": {"summary": 'Астана', "value": {
        "title": "Астана 4 звезды",
        "location": "Астана, Ул. Пушкина, д. Колотушкина",
    }},
})):
    data = await db.hotel.add(hotel_data)
    await db.commit()
    return {"status": "success", "data": data}


@router.put("/{hotel_id}", summary='Изменение отеля')
async def edit_hotel(hotel_id: int,
                     hotel_data: HotelAdd,
                     db: DBDep):
    try:
        await db.hotel.edit(hotel_data, id=hotel_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}


@router.patch("/{hotel_id}",
              summary='Частичное обновление данных об отеле',
              description='Частичное обновление какого либо значения отеля: можно отправить и name, и title')
async def update_hotel(hotel_id: int,
                       hotel_data: HotelPatch,
                       db: DBDep):
    try:
        await db.hotel.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}
