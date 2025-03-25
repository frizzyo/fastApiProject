from app.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    second_name: Mapped[str | None] = mapped_column(String(100))
    nickname: Mapped[str | None] = mapped_column(String(100))
