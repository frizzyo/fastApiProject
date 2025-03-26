from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from pydantic import EmailStr

from app.repos.base import BaseRepository
from app.models.users import UsersOrm
from app.schemas.users import User, UserAdd, UserWithHashedPassword


class UserRepos(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserAdd):
        try:
            await super().add(data)
        except IntegrityError:
            raise ValueError(f"Пользователь с таким email - ({data.email}) уже существуют")

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashedPassword.model_validate(model)
