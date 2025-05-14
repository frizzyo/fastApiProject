import json
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database import Base, engine_null_pool
from app.main import app
from app.models import *


@pytest.fixture(scope="session", autouse=True)
async def create_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def fill_database(create_database):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "email": "kot@pec.com",
            "password": "kotopec"
        })
        with open(f"{Path(__file__).parent/'mock_hotels.json'}", encoding="utf-8") as file:
            hotels_data = json.load(file)
            for hotel in hotels_data:
                await ac.post(
                    "/hotels/",
                    json={
                        "title": hotel["title"],
                        "location": hotel["location"],
                    }
                )

        with open(f"{Path(__file__).parent/'mock_rooms.json'}", encoding="utf-8") as file:
            rooms_data = json.load(file)
            for room in rooms_data:
                await ac.post(
                    f"/hotels/{room['hotel_id']}/rooms/",
                    json={
                        "title": room["title"],
                        "description": room["description"],
                        "price": room["price"],
                        "quantity": room["quantity"],
                    }
                )
