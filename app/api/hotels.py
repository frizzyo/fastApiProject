from typing import Annotated

from fastapi import APIRouter, Query, Body, Depends
from app.schemas.hotels import Hotel, HotelPatch
from app.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, 'title': 'Сочи', 'name': 'sochi'},
    {"id": 2, 'title': 'Дубай', 'name': 'dubai'},
    {"id": 3, 'title': 'Казань', 'name': 'kazan'},
    {"id": 4, 'title': 'Питер', 'name': 'spb'},
    {"id": 5, 'title': 'Балашиха', 'name': 'balaha'},
    {"id": 6, 'title': 'Сызрань', 'name': 'sizran'},
    {"id": 7, 'title': 'Мурманск', 'name': 'murmansk'},
    {"id": 8, 'title': 'Астана', 'name': 'astana'},
    {"id": 9, 'title': 'Череповец', 'name': 'cherepovec'},
    {"id": 10, 'title': 'Дубай2', 'name': 'dubai2'},
]


@router.get("/", summary='Получение списка отелей')
def get_hotels(
        pagination_params: PaginationDep,
        id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description='Name of the hotel'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if name and hotel['name'] != name:
            continue
        hotels_.append(hotel)
    if pagination_params.page and pagination_params.per_page:
        return hotels_[(pagination_params.page - 1) * pagination_params.per_page:
                       pagination_params.page * pagination_params.per_page]
    return hotels_


@router.delete("/{id}", summary='Удаление отеля')
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "success", "data": hotels}


@router.post("/", summary='Добавление отеля')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": 'Москва', "value": {
        "title": "Москва",
        "name": "Moscow",
    }},
    "2": {"summary": 'Астана', "value": {
        "title": "Астана",
        "name": "Astana",
    }},
})):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name

    })
    return {"status": "success", "data": hotels}


@router.put("/{hotel_id}", summary='Изменение отеля')
def update_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = hotel_data.name
            hotel["title"] = hotel_data.title
            return {'status': 'success', 'data': hotels}


@router.patch("/{hotel_id}",
              summary='Частичное обновление данных об отеле',
              description='Частичное обновление какого либо значения отеля: можно отправить и name, и title')
def update_hotel(hotel_id: int, hotel_data: HotelPatch):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {'status': 'success', 'data': hotels}
