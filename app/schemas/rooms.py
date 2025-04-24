from pydantic import BaseModel, Field, ConfigDict

from app.schemas.facilities import Facilities


class RoomAttributes(BaseModel):
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAdd(RoomAttributes):
    hotel_id: int
    title: str


class RoomAddRequest(RoomAttributes):
    title: str
    facilities_ids: list[int] = []


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facilities]


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatchRequest(RoomPatch):
    facilities_ids: list[int] = []
