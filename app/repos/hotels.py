from sqlalchemy import select
from sqlalchemy.sql.operators import ilike_op

from app.repos.base import BaseRepository
from app.models.hotels import HotelsOrm
from app.schemas.hotels import Hotel


class HotelsRepos(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      title,
                      location,
                      limit,
                      offset) -> list[Hotel]:
        query = select(self.model)
        if location:
            query = query.filter(ilike_op(HotelsOrm.location, f'%{location.strip()}%'))
        if title:
            query = query.filter(ilike_op(HotelsOrm.title, f'%{title.strip()}%'))
        # Такое выполнится быстрее при большом количестве данных в таблице
        # if location:
        #     query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower())))
        # if title:
        #     query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower())))
        query = (
            query
            .limit(limit)
            .offset(offset)
            .order_by('id')
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]
