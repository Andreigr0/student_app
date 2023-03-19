import datetime

from pydantic import BaseModel, Field

from shared.schemas import ValueSchema


class Review(BaseModel):
    from companies.schemas import CompanyShort

    id: int
    rating: int = Field(title='Оценка', ge=1, le=5)
    date: datetime.date = Field(title='Дата отзыва')
    role: str = Field(title='Роль в проекте')
    text: str | None = Field(title='Текст отзыва')
    company: CompanyShort = Field(title='Компания, которая разместила проект')


class ReviewDetails(Review):
    project: ValueSchema = Field(title='Проект')
    start_date: datetime.date = Field(title='Дата начала проекта')
    finish_date: datetime.date = Field(title='Дата завершения проекта')
    spent_hours: int = Field(title='Потраченные часы')
