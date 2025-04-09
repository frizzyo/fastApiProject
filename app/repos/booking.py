from pydantic import BaseModel
from sqlalchemy import insert

from app.repos.base import BaseRepository
from app.repos.rooms import RoomsRepos
from app.models.bookings import BookingsOrm
from app.schemas.bookings import Booking


class BookingsRepos(BaseRepository):
    model = BookingsOrm
    schema = Booking
