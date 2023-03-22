import enum
from dataclasses import dataclass
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class ValueSchema(BaseModel):
    id: int
    name: str


class FileSchema(BaseModel):
    name: str
    url: str


class SemesterType(enum.Enum):
    fall = 'fall'
    spring = 'spring'


class Semester(BaseModel):
    year: int
    semester_type: SemesterType


@dataclass
class SemesterQuery:
    year: int | None = Query(default=None, description='Год', ge=1950, le=datetime.now().year)
    semester_type: SemesterType | None = Query(default=None, description='Семестр')


@dataclass
class PaginationQuery:
    page: int = Query(default=1, description='Страница', ge=1)
    per_page: int = Query(default=10, description='Количество элементов на странице', ge=1, le=100)
