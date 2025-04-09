import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path


from app.api.hotels import router as hotels_router
from app.api.auth import router as auth_router
from app.api.rooms import router as room_router
from app.api.bookings import router as booking_router

sys.path.append(str(Path(__file__).parent.parent))
app = FastAPI()


app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(booking_router)


if __name__ == "__main__":
    uvicorn.run(app='app.main:app', reload=True)
