from datetime import date

from app.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    # create
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        date_from=date(2024, 1, 1),
        date_to=date(2025, 1, 1),
        user_id=user_id,
        price=100,
    )
    booking_creat = await db.bookings.add(booking_data)
    # get
    booking_get = await db.bookings.get_one_or_none(id=booking_creat.id)
    assert booking_get
    assert booking_get.id == booking_creat.id
    assert booking_get.user_id == booking_creat.user_id
    # update
    booking_data.price = 662
    booking_update = await db.bookings.edit(
        booking_data,
        id=booking_get.id
    )
    assert booking_update
    assert booking_update.price == 662
    # delete
    await db.bookings.delete(id=booking_creat.id)
    booking = await db.bookings.get_one_or_none(id=booking_creat.id)
    assert not booking
