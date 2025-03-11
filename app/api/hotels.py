from fastapi import APIRouter, Query, Body
from sqlalchemy import Insert, Select
from sqlalchemy.sql.operators import ilike_op

from app.schemas.hotels import Hotel, HotelPatch
from app.api.dependencies import PaginationDep
from app.database import async_session_maker, engine
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, 'title': 'Сочи', 'name': 'sochi'},
    {"id": 2, 'title': 'Дубай', 'name': 'dubai'},
    {"id": 3, 'title': 'Казань', 'name': 'kazan'},
    {"id": 4, 'title': 'Питер', 'name': 'spb'},
    {"id": 5, 'title': 'Балашиха', 'name': 'balaha'},
    {"id": 6, 'title': 'Сызрань', 'name': 'sizran'},
    {"id": 7, 'title': 'Мурманск', 'name': 'murmansk'},
    {"id": 8, 'title': 'Астана', 'name': 'astana'},
    {"id": 9, 'title': 'Череповец', 'name': 'cherepovec'},
    {"id": 10, 'title': 'Дубай2', 'name': 'dubai2'},
]


@router.get("/", summary='Получение списка отелей')
async def get_hotels(
        pagination_params: PaginationDep,
        title: str | None = Query(None, description='Name of the hotel'),
        location: str | None = Query(None, description='Location of the hotel'),
):
    per_page = pagination_params.per_page or 5
    async with async_session_maker() as session:
        query = Select(HotelsOrm)
        if location:
            query = query.filter(ilike_op(HotelsOrm.location, f'%{location}%'))
        if title:
            query = query.filter(ilike_op(HotelsOrm.title, f'%{title}%'))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination_params.page - 1))
        )
        result = await session.execute(query)
        hotels_ = result.scalars().all()

    return hotels_


@router.delete("/{id}", summary='Удаление отеля')
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "success", "data": hotels}


@router.post("/", summary='Добавление отеля')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": 'Москва', "value": {
        "title": "Москва 5 звезд",
        "location": "Ул. Пушкина, д. Колотушкина",
    }},
    "2": {"summary": 'Астана', "value": {
        "title": "Астана 4 звезды",
        "location": "Астана, Ул. Пушкина, д. Колотушкина",
    }},
})):
    async with async_session_maker() as session:
        add_hotel_stmt = Insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "success"}


@router.put("/{hotel_id}", summary='Изменение отеля')
def update_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = hotel_data.name
            hotel["title"] = hotel_data.title
            return {'status': 'success', 'data': hotels}


@router.patch("/{hotel_id}",
              summary='Частичное обновление данных об отеле',
              description='Частичное обновление какого либо значения отеля: можно отправить и name, и title')
def update_hotel(hotel_id: int, hotel_data: HotelPatch):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {'status': 'success', 'data': hotels}
