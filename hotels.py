import uvicorn
from fastapi import APIRouter, Query, Body

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
    hotel = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "success", "data": hotel}

@router.post("/", summary='Добавление отеля')
def create_hotel(
        title: str = Body(embed=True, description='Name of the hotel', title='Name of the hotel'),
):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "name": title
    })
    return {"status": "success", "data": hotels}


@router.put("/{id}", summary='Изменение отеля')
def update_hotel(
        id: int,
        title: str = Body(),
        name: str = Body(),
):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["name"] = name
            hotel["title"] = title
            return {'status': 'success'}


@router.patch("/{id}",
              summary='Частичное обновление даннхы об отеле',
              description='Частичное обновление какого либо значения отеля: можно отправить и name, и title')
def update_hotel(
        id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True),
):
    for hotel in hotels:
        if hotel["id"] == id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return {'status': 'success'}