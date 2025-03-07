from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1, description="Hotel page number")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Hotel page size")]


PaginationDep = Annotated[PaginationParams, Depends()]
