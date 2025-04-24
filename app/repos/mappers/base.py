from typing import TypeVar

from pydantic import BaseModel

from app.database import Base

DBModelType = TypeVar('DBModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)

    @classmethod
    def map_to_persistent_entity(cls, schema):
        return cls.db_model(**schema.model_dump())
