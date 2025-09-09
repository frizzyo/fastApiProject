from datetime import date

from sqlalchemy import select, insert

from app.repos.base import BaseRepository
from app.models.bookings import BookingsOrm
from app.repos.utils import rooms_ids_for_booking
from app.repos.mappers.mappers import BookingDataMapper


class BookingsRepos(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from==date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: model):
        rooms_id = rooms_ids_for_booking(date_from=data.date_from, date_to=data.date_to)
        if data.room_id not in rooms_id:
            raise Exception
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        data = await self.session.execute(query)
        model = data.scalars().one()
        return self.mapper.map_to_domain_entity(model)

