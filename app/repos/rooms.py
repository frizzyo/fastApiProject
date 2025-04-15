from sqlalchemy import select, func
from sqlalchemy.sql.operators import ilike_op

from app.database import engine
from app.models.bookings import BookingsOrm
from app.repos.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.repos.utils import rooms_ids_for_booking
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
        rooms_id = rooms_ids_for_booking(date_from, date_to, hotel_id)
        # print(rooms_id.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_id))
