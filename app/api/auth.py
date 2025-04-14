from fastapi import APIRouter, HTTPException, Response, Request

from app.api.dependencies import UserIdDep, DBDep
from app.schemas.users import UserRequestAdd, UserAdd, UserLogin
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e))
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response,
        db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не существует")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie('access_token', access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"data": user}


@router.post("/logout")
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "Ok"}
