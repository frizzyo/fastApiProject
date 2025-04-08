from pydantic import BaseModel, Field, ConfigDict


class RoomAttributes(BaseModel):
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAdd(RoomAttributes):
    title: str


class Room(RoomAdd):
    hotel_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
