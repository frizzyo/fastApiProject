from sqlalchemy import select
from sqlalchemy.sql.operators import ilike_op
from sqlalchemy.orm import selectinload

from app.database import engine
from app.repos.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.repos.mappers.mappers import RoomsDataMapper
from app.repos.utils import rooms_ids_for_booking
from app.schemas.rooms import Room, RoomWithRels


class RoomsRepos(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_hotel_filtered(self,
                                 title,
                                 hotel_id) -> list[Room]:
        query = select(self.model).filter(RoomsOrm.hotel_id == hotel_id)
        if title:
            query = query.filter(ilike_op(RoomsOrm.title, f"%{title.strip()}%"))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_from,
                                   date_to):
        rooms_id = rooms_ids_for_booking(date_from, date_to, hotel_id)
        # print(rooms_id.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_id))
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
