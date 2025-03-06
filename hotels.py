from fastapi import APIRouter, Query, Body
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, 'title': 'Sochi', 'name': 'sochi'},
    {"id": 2, 'title': 'Dubai', 'name': 'dubai'},
]


@router.get("/", summary='Получение списка отелей')
def get_hotels(
        id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description='Name of the hotel', title='Name of the hotel'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if name and hotel['name'] != name:
            continue
        hotels_.append(hotel)
    return hotels_


@router.delete("/{id}", summary='Удаление отеля')
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "success", "data": hotels}


@router.post("/", summary='Добавление отеля')
def create_hotel(hotel_data: Hotel):
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
