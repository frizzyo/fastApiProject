from pydantic import BaseModel, Field, ConfigDict


class FacilitiesAdd(BaseModel):
    name: str


class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)