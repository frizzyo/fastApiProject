import jwt
from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.schemas.users import UserRequestAdd, UserAdd
from app.repos.users import UserRepos
from app.database import async_session_maker
from app.config import settings


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire}) ## |= == .update
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


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


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UserRepos(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не существует")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie('access_token', access_token)
        return {"access_token": access_token}
