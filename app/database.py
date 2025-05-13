import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text, NullPool

from app.config import settings


engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

# сырой запрос
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("select version()"))
#         print(res.fetchone())
#
# asyncio.create_task(func())

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
