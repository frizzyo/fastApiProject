import json
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database import Base, engine_null_pool, async_session_maker_null_pool
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def create_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels_data = json.load(file)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]

    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms_data = json.load(file)
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def fill_database(create_database):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "email": "kot@pec.com",
            "password": "kotopec"
        })
