from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from pydantic import BaseModel

from app.exceptions import NotFound, MultipleResult
from app.repos.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def _check_result(self, **filter_by):  ## проверка количества вернувшихся значений
        query = select(self.model).filter_by(**filter_by)
        qdata = await self.session.execute(query)
        try:
            qdata.scalars().one()
        except NoResultFound:
            raise NotFound
        except MultipleResultsFound:
            raise MultipleResult

    async def get_filtered(self, *args, **kwargs) -> list[BaseModel]:
        query = (select(self.model)
                 .filter(*args)
                 .filter_by(**kwargs))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        data = await self.session.execute(query)
        model = data.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        query = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(query)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        await self._check_result(**filter_by)
        upd_query = (update(self.model)
                     .filter_by(**filter_by)
                     .values(**data.model_dump(exclude_unset=exclude_unset))).returning(self.model)
        data = await self.session.execute(upd_query)
        return self.mapper.map_to_domain_entity(data.scalars().one())

    async def delete(self, *args, **kwargs):
        # await self._check_result(**kwargs)
        del_query = delete(self.model).filter(*args).filter_by(**kwargs)
        await self.session.execute(del_query)
