import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as hotels_router
from app.config import settings

app = FastAPI()

app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run(app='main:router', reload=True)
