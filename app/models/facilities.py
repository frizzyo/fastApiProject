from app.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id = mapped_column(ForeignKey("rooms.id"))
    facilities_id = mapped_column(ForeignKey("facilities.id"))
