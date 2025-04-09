from fastapi import APIRouter, Query, Body, HTTPException, Request

from app.schemas.bookings import BookingAdd, BookingRequest
from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import NotFound, MultipleResult
from app.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/", summary='Добавление бронирования')
async def create_booking(db: DBDep, booking_data: BookingRequest, request: Request):
    _user_id = AuthService().decode_token(request.cookies.get("access_token")).get("user_id")
    _room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=_user_id, price=_room.price, **booking_data.model_dump())
    data = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "success", "data": data}
