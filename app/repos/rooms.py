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
                      title) -> list[Room]:
        query = select(self.model)
        if title:
            query = query.filter(ilike_op(RoomsOrm.title, f"%{title.strip()}%"))
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

    async def add(self, hotel_id: int, data: BaseModel):
        query = insert(self.model)
        query = query.values(hotel_id=hotel_id, **data.model_dump()).returning(self.model)
        data = await self.session.execute(query)
        model = data.scalars().one()
        return self.schema.model_validate(model)
