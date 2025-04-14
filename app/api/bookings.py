from fastapi import APIRouter, Query, Body, HTTPException, Request

from app.schemas.bookings import BookingAdd, BookingRequest
from app.api.dependencies import PaginationDep, DBDep, UserIdDep
from app.exceptions import NotFound, MultipleResult
from app.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/", summary="Все бронирования")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Все бронирования пользователя")
async def get_bookings_filtered(db: DBDep,
                                user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("/", summary='Добавление бронирования')
async def create_booking(db: DBDep,
                         user_id: UserIdDep,
                         booking_data: BookingRequest):
    _room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        price=_room.price,
        **booking_data.model_dump())
    data = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "success", "data": data}
