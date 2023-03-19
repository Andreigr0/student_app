import datetime

from pydantic import BaseModel, Field

from shared.schemas import FileSchema, ValueSchema


class PublicStudent(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None
    course: str
    group: str
    birth_date: datetime.date
    contacts: list[str] | None
    training_direction: str = Field(title='Направление подготовки')
    training_profile: str = Field(title='Профиль')
    faculty: str = Field(title='Факультет')
    cathedra: str = Field(title='Кафедра')
    training_form: str = Field(title='Форма обучения')

    about: str | None = Field(title='О себе')
    resume: FileSchema | None = Field(title='Резюме')


class PersonalStudent(PublicStudent):
    record_book_number: str = Field(title='Номер зачетной книжки')
    document_number: str = Field(title='Документ (паспорт)')
    snils: str = Field(title='СНИЛС')
    relatives: list[str] | None = Field(default=None, title='Родственники')


class StudentCompetencies(BaseModel):
    skills: list[ValueSchema] = Field(title='Навыки')
    subject_areas: list[ValueSchema] = Field(title='Предметные области')


class UpdateStudentCompetencies(BaseModel):
    skills: list[int] | None = Field(title='Навыки')
    subject_areas: list[int] | None = Field(title='Предметные области')


class Portfolio(BaseModel):
    id: int
    name: str = Field(title='Название')
    file: FileSchema
    discipline: str | None = Field(title='Дисциплина')
    evaluation: str | None = Field(title='Оценка')
    semester: str | None = Field(title='Семестр')
    stage: str | None = Field(title='Этап')
    type: str | None = Field(title='Тип')
    plagiarism: int | None = Field(title='Плагиат в %')
    is_introduction_practice: bool = Field(default=False, title='Ознакомительная практика')


class StudentPortfolio(BaseModel):
    course_projects: list[Portfolio] = Field(title='Курсовые проекты')
    practices: list[Portfolio] = Field(title='Практики')
    abstracts: list[Portfolio] = Field(title='Рефераты')
    group_project_learning: list[Portfolio] = Field(title='Групповое проектное обучение')
    scientific_activity_results: list[Portfolio] = Field(title='Результаты научной деятельности')
    graduate_qualification_works: list[Portfolio] = Field(title='Выпускные квалификационные работы')
