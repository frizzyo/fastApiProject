from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.schemas.facilities import FacilitiesAdd, Facilities
from app.api.dependencies import DBDep
from app.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Интересы"])


@router.get("/", summary="Все интересы")
@cache(expire=30)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/", summary='Добавление интересов')
async def create_facilities(db: DBDep,
                            facilities_data: FacilitiesAdd):
    data = await db.facilities.add(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status": "success", "data": data}
