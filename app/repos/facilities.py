from sqlalchemy import select, delete, insert

from app.repos.base import BaseRepository
from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.repos.mappers.mappers import FacilitiesDataMapper, RoomsFacilitiesDataMapper


class FacilitiesRepos(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomFacilitiesRepos(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomsFacilitiesDataMapper

    async def set_room_facilities(self,
                                  room_id: int,
                                  facilities_ids: list[int]) -> None:
        query = (
            select(self.model.facilities_id).filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_facilities_ids = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_append: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facilities_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_facilities_stmt)

        if ids_to_append:
            insert_facilities_stmt = (
                insert(self.model)
                .values(
                    [{"room_id": room_id, "facilities_id": f_id} for f_id in ids_to_append]
                )
            )
            await self.session.execute(insert_facilities_stmt)
