from datetime import date

from sqlalchemy import select
from sqlalchemy.sql.operators import ilike_op

from app.models.rooms import RoomsOrm
from app.repos.base import BaseRepository
from app.models.hotels import HotelsOrm
from app.repos.mappers.mappers import HotelDataMapper
from app.repos.utils import rooms_ids_for_booking


class HotelsRepos(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date,
                                   limit: int,
                                   offset: int,
                                   title: str,
                                   location: str
                                   ):
        rooms_id = rooms_ids_for_booking(date_from, date_to)

        hotels_id = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_id))
        )
        query = select(self.model).filter(HotelsOrm.id.in_(hotels_id))
        if title:
            query = query.filter(ilike_op(HotelsOrm.title, f'%{title.strip()}%'))
        if location:
            query = query.filter(ilike_op(HotelsOrm.location, f'%{location.strip()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
            .order_by('id')
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
