from app.repos.base import BaseRepository
from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.schemas.facilities import Facilities, RoomsFacilities


class FacilitiesRepos(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomFacilitiesRepos(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities
