from fastapi import APIRouter

from app.schemas.facilities import FacilitiesAdd, Facilities
from app.api.dependencies import DBDep
from app.exceptions import NotFound, MultipleResult

router = APIRouter(prefix="/facilities", tags=["Интересы"])


@router.get("/", summary="Все интересы")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/", summary='Добавление интересов')
async def create_facilities(db: DBDep,
                            facilities_data: FacilitiesAdd):
    data = await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "success", "data": data}
