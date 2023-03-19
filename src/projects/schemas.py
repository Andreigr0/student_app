import datetime
import enum

from pydantic import BaseModel, Field

from shared.schemas import ValueSchema


class Project(BaseModel):
    from companies.schemas import CompanyShort

    id: int
    name: str = Field(..., title='Название проекта')
    status: str | None = Field(default=None, title='Статус проекта')
    finish_date: datetime.date | None = Field(default=None, title='Дата завершения проекта')
    competences: list[ValueSchema] | None = Field(default=None, title='Компетенции, необходимые для проекта')

    duration: int = Field(..., ge=1, title='Продолжительность проекта в днях')
    type: str | None = Field(default=None, title='Тип проекта')
    view: str | None = Field(default=None, title='Вид проекта')
    company: CompanyShort = Field(..., title='Компания, которая разместила проект')


class ProjectStage(BaseModel):
    id: int
    name: str
    start_date: datetime.date
    finish_date: datetime.date


class ProjectPosition(str, enum.Enum):
    """Должность в проекте"""

    student = 'student'
    curator = 'curator'
    company = 'company'


class ProjectMember(BaseModel):
    id: int
    avatar: str | None
    name: str
    description: str
    role: ProjectPosition


class ProjectRole(BaseModel):
    id: int
    name: str
    work_load: str = Field(..., title='Загрузка')
    work_format: str = Field(..., title='Формат работы')
    needed_competencies: list[ValueSchema] = Field(..., title='Требуемые компетенции')
    acquired_competencies: list[ValueSchema] = Field(...,
                                                     title='Компетенции, которые получит студент по итогам работы')


class ProjectDetails(Project):
    from companies.schemas import CompanyShort

    start_date: datetime.date = Field(..., title='Дата начала проекта')
    finish_date: datetime.date = Field(..., title='Дата завершения проекта')
    is_only_for_digital_academy: bool = Field(..., title='Проект доступен только для студентов цифровой академии')
    description: str = Field(..., title='Описание проекта')
    roles: list[ProjectRole] = Field(..., title='Роли')
    solving_problems: str = Field(..., title='Решаемые проблемы')
    goals: str = Field(..., title='Цели')
    tasks: str = Field(..., title='Задачи')
    results: str = Field(..., title='Результат')
    what_will_participant_get: str = Field(..., title='Что получит участник')
    stages: list[ProjectStage] = Field(..., title='Этапы и сроки проекта')
    companies: list[CompanyShort] = Field(..., title='Компании организаторы и партнёры')
    team: list[ProjectMember] = Field(..., title='Команда')
    other_projects: list[Project] = Field(..., title='Другие проекты этой области')

    is_applied: bool = Field(default=False,
                             title='Признак того, что пользователь подал заявку на участие в проекте')
    attach_report_last_date: datetime.date | None = Field(default=None,
                                                          title='Дата, до которой можно прикрепить отчёт')


class ParticipationCreate(BaseModel):
    role_id: int = Field(..., ge=1, title='Id роли')
    about: str = Field(..., title='О себе')
    competencies: str = Field(..., title='Компетенции и личные качества')
    experience: str = Field(..., title='Опыт')
