from app.repos.base import BaseRepository
from app.models.facilities import FacilitiesOrm
from app.schemas.facilities import Facilities


class FacilitiesRepos(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
