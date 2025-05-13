from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.hotels import router as hotels_router
from app.api.auth import router as auth_router
from app.api.rooms import router as room_router
from app.api.bookings import router as booking_router
from app.api.facilities import router as facility_router
from app.api.images import router as image_router
from app.init import redis_manager

sys.path.append(str(Path(__file__).parent.parent))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(facility_router)
app.include_router(image_router)


if __name__ == "__main__":
    uvicorn.run(app='app.main:app', reload=True)
