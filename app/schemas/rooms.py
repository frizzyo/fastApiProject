from pydantic import BaseModel, Field, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatchRequest(RoomPatch):
    facilities_ids: list[int] = []
