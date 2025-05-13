import os
from pathlib import Path
from time import sleep

from PIL import Image

from app.tasks.celery_app import celery_app


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

