import datetime

from pydantic import BaseModel, Field

from shared.schemas import Semester


class DayAttendance(BaseModel):
    date: datetime.date
    percent: float


class SubjectPercent(BaseModel):
    short_name: str = Field(title='Краткое название предмета')
    full_name: str = Field(title='Полное название предмета')
    percent: float = Field(title='Процент посещаемости')


class MissedLesson(BaseModel):
    date: datetime.date = Field(title='Дата пропуска')
    subject: str = Field(title='Предмет')
    type: str = Field(title='Тип занятия (лекция, практика, лабораторная)')


class Attendance(BaseModel):
    semester: Semester = Field(title='Семестр')
    by_days: list[DayAttendance] = Field(title='Посещаемость по дням')
    by_subjects: list[SubjectPercent] = Field(title='Посещаемость по дисциплинам')
    missed_lessons: list[MissedLesson] = Field(title='Пропущенные занятия')
