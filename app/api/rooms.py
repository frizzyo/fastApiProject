from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from app.api.dependencies import DBDep
from app.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest
from app.schemas.facilities import RoomsFacilitiesAdd
from app.exceptions import NotFound, MultipleResult

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("/{room_id}", summary="Получение 1 номера по его id")
async def get_room_by_id(hotel_id: int,
                         room_id: int,
                         db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.get("/", summary='Получение списка номеров')
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date,
        date_to: date,
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.delete("/{room_id}", summary='Удаление номера')
async def delete_room(hotel_id: int,
                      room_id: int,
                      db: DBDep):
    try:
        await db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {"status": "success"}


@router.post("/", summary='Добавление отеля')
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": '2ух местный, вид на море', "value": {
        "title": "2ух местный",
        "description": "2ух местный номер с видом на море",
        "price": 1500,
        "quantity": 3,
    }},
    "2": {"summary": 'Одноместный, вид на горы', "value": {
        "title": "Одноместный местный",
        "price": 1100,
        "quantity": 6,
    }},
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    data = await db.rooms.add(_room_data)
    room_facilities_data = [RoomsFacilitiesAdd(room_id=data.id, facilities_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {"status": "success", "data": data}


@router.put("/{room_id}", summary='Изменение отеля')
async def edit_room(hotel_id: int,
                    room_id: int,
                    db: DBDep,
                    room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(_room_data, id=room_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}


@router.patch("/{room_id}",
              summary='Частичное обновление данных о номере',
              description='Частичное обновление какого либо значения номера')
async def update_room(hotel_id: int,
                      room_id: int,
                      db: DBDep,
                      room_data: RoomPatch):
    try:
        await db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await db.commit()
    except NotFound:
        raise HTTPException(status_code=404, detail="Нет записи для такого id")
    except MultipleResult:
        raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}
