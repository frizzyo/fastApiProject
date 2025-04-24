from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserInfo(BaseModel):
    email: EmailStr
    first_name: str | None = Field(None)
    second_name: str | None = Field(None)
    nickname: str | None = Field(None)


class UserRequestAdd(UserInfo):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdd(UserInfo):
    hashed_password: str


class User(UserInfo):
    id: int


class UserWithHashedPassword(User):
    hashed_password: str
