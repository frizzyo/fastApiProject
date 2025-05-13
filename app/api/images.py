import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    with open(f"{Path(__file__).parent.parent/'static/images'}/{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(f"{Path(__file__).parent.parent/'static/images'}/{file.filename}")
