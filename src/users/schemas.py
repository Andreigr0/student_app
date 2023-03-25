from datetime import date

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: str
    login: str = Field()


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None = None
    login: str | None = None
    password: str | None = None
    birth_date: date | None = None
    first_name: str | None = None
    is_active: bool | None = None


class StudentCreate(UserCreate):
    group_id: int
