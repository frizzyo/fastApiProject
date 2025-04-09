from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from app.database import async_session_maker
from app.services.auth import AuthService
from app.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="page number")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="page size")]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail='Token is missing')
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
