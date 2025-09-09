import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_db
from app.config import settings
from app.database import Base, engine_null_pool, async_session_maker_null_pool
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def create_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels_data = json.load(file)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]

    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms_data = json.load(file)
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.hotels.add_bulk(hotels)
        await _db.rooms.add_bulk(rooms)
        await _db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def fill_database(create_database, ac):
    await ac.post("/auth/register", json={
        "email": "kot@pec.com",
        "password": "kotopec"
    })


@pytest.fixture(scope="session")
async def authenticated_ac(fill_database, ac):
    token = await ac.post("/auth/login", json={"email": "kot@pec.com", "password": "kotopec"})
    assert token.cookies["access_token"]
    me = await ac.get("/auth/me", cookies={"access_token": token.json()["access_token"]})
    assert me.json()["data"]["email"] == "kot@pec.com"
    yield ac
