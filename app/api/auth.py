from fastapi import APIRouter, HTTPException, Response

from app.schemas.users import UserRequestAdd, UserAdd
from app.repos.users import UserRepos
from app.database import async_session_maker
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UserRepos(session).add(new_user_data)
        except Exception as e:
            raise HTTPException(status_code=418, detail=str(e))
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UserRepos(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не существует")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie('access_token', access_token)
        return {"access_token": access_token}
