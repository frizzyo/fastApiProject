from app.repos.base import BaseRepository
from app.models.rooms import RoomsOrm


class RoomsRepos(BaseRepository):
    model = RoomsOrm
