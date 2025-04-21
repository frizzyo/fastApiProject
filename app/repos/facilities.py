from app.repos.base import BaseRepository
from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.schemas.facilities import Facilities, RoomsFacilities, RoomsFacilitiesAdd


class FacilitiesRepos(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomFacilitiesRepos(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities

    async def update(self,
                     room_id: int,
                     data):
        await self.delete(room_id=room_id)
        await self.add_bulk(data)
