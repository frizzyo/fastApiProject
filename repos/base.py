from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def _check_result(self, **filter_by):  ## проверка количества вернувшихся значений
        query = select(self.model).filter_by(**filter_by)
        qdata = await self.session.execute(query)
        try:
            qdata.scalars().one()
        except NoResultFound as ex:
            raise NoResultFound
        except MultipleResultsFound as ex:
            raise MultipleResultsFound

    async def get_one(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        data = await self.session.execute(query)
        return data.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False,**filter_by):
        await self._check_result(**filter_by)
        upd_query = (update(self.model)
                     .filter_by(**filter_by)
                     .values(**data.model_dump(exclude_unset=exclude_unset)))
        await self.session.execute(upd_query)

    async def delete(self, **filter_by):
        await self._check_result(**filter_by)
        del_query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(del_query)
