from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.sql.operators import ilike_op

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
