from sqlalchemy.exc import IntegrityError

from app.repos.base import BaseRepository
from app.models.users import UsersOrm
from app.schemas.users import User, UserAdd


class UserRepos(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserAdd):
        try:
            await super().add(data)
        except IntegrityError as e:
            raise ValueError(f"Пользователь с таким email - {data.email} уже существуют")
