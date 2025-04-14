from sqlalchemy import select, func
from sqlalchemy.sql.operators import ilike_op

from app.database import engine
from app.models.bookings import BookingsOrm
from app.repos.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepos(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      title,
                      hotel_id) -> list[Room]:
        query = select(self.model).filter(RoomsOrm.hotel_id == hotel_id)
        if title:
            query = query.filter(ilike_op(RoomsOrm.title, f"%{title.strip()}%"))
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_from,
                                   date_to):
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(RoomsOrm.id.label("room_id"),
                   (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"))
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left")
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery()
        )

        rooms_id = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0,
                    rooms_left_table.c.room_id.in_(rooms_ids_for_hotel))
        )
        # print(rooms_id.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_id))
