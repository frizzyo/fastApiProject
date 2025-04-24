from app.repos.base import BaseRepository
from app.models.bookings import BookingsOrm
from app.repos.mappers.mappers import BookingDataMapper


class BookingsRepos(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
