from fastapi import APIRouter, Query, Body, HTTPException

from app.schemas.rooms import RoomPatch, RoomAdd
from app.database import async_session_maker
from app.repos.rooms import RoomsRepos
from app.exceptions import NotFound, MultipleResult

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("/rooms/{room_id}", summary="Получение 1 номера по его id")
async def get_hotel_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepos(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.get("/", summary='Получение списка номеров')
async def get_hotels(
        hotel_id: int,
        title: str | None = Query(None),
):
    async with async_session_maker() as session:
        return await RoomsRepos(session).get_all(
            title=title
        )


@router.delete("/{room_id}", summary='Удаление номера')
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        try:
            await RoomsRepos(session).delete(hotel_id=hotel_id, id=room_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {"status": "success"}


@router.post("/", summary='Добавление отеля')
async def create_hotel(hotel_id: int, hotel_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        data = await RoomsRepos(session).add(hotel_id, hotel_data)
        await session.commit()
    return {"status": "success", "data": data}


@router.put("/{room_id}", summary='Изменение отеля')
async def edit_hotel(hotel_id: int,
                     room_id: int,
                     hotel_data: RoomAdd):
    async with async_session_maker() as session:
        try:
            await RoomsRepos(session).edit(hotel_data, id=room_id, hotel_id=hotel_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}


@router.patch("/{room_id}",
              summary='Частичное обновление данных о номере',
              description='Частичное обновление какого либо значения номера')
async def update_hotel(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with async_session_maker() as session:
        try:
            await RoomsRepos(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
            await session.commit()
        except NotFound:
            raise HTTPException(status_code=404, detail="Нет записи для такого id")
        except MultipleResult:
            raise HTTPException(status_code=400, detail="Найдено более одной записи для такого id")
    return {'status': 'success'}
