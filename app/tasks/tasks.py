import asyncio
import os
from pathlib import Path
from time import sleep

from PIL import Image

from app.database import async_session_maker_null_pool
from app.tasks.celery_app import celery_app
from app.utils.db_manager import DBManager


@celery_app.task
def test_task():
    sleep(6)
    print("Ну все типо")


@celery_app.task
def resize_image(image_path):
    sizes = [1000, 500, 300]
    output_folder = f"{Path(__file__).parent.parent/'static/images'}"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        new_filename = name + str(size) + ext

        output_path = os.path.join(output_folder, new_filename)

        img_resized.save(output_path)

    print(f"Я всё")


async def get_booking_with_today_checkin_helper():
    print("Набалтываю!!!")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_booking_with_today_checkin()
        print(f"{bookings}")


@celery_app.task(name='booking_today_checkin')
def send_emails_to_user_with_today_checkin():
    asyncio.run(get_booking_with_today_checkin_helper())