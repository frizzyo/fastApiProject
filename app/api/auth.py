from fastapi import APIRouter
from passlib.context import CryptContext

from app.schemas.users import UserRequestAdd, UserAdd
from app.repos.users import UserRepos
from app.database import async_session_maker


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UserRepos(session).add(new_user_data)
        except Exception as e:
            return {"error": str(e)}
        await session.commit()
    return {"status": "OK"}
