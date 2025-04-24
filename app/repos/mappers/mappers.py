from app.models.bookings import BookingsOrm
from app.models.facilities import RoomsFacilitiesOrm, FacilitiesOrm
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.models.users import UsersOrm
from app.repos.mappers.base import DataMapper
from app.schemas.bookings import Booking
from app.schemas.facilities import RoomsFacilities, Facilities
from app.schemas.hotels import Hotel
from app.schemas.rooms import Room
from app.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacilities


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User
