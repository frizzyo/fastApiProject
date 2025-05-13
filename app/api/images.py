import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, BackgroundTasks

from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    path = f"{Path(__file__).parent.parent/'static/images'}/"
    with open(f"{path}{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(f"{path}{file.filename}")
    # background_tasks.add_task(resize_image, f"{path}{file.filename}")
