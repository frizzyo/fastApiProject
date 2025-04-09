from app.repos.hotels import HotelsRepos
from app.repos.rooms import RoomsRepos
from app.repos.users import UserRepos
from app.repos.booking import BookingsRepos


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotel = HotelsRepos(self.session)
        self.rooms = RoomsRepos(self.session)
        self.users = UserRepos(self.session)
        self.bookings = BookingsRepos(self.session)

        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
