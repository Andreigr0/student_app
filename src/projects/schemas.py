import datetime
import enum
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field

from shared.schemas import ValueSchema


class ProjectsCategory(str, enum.Enum):
    """Категория проектов (Активные, Завершенные)"""

    active = 'active'
    finished = 'finished'


class ProjectStatus(str, enum.Enum):
    """Статус проекта (Идёт набор, Команда набрана, Завершен, Снят с публикации)"""
    under_recruitment = 'under_recruitment'
    recruited = 'recruited'
    finished = 'finished'
    withdrawn = 'withdrawn'


class ProjectType(str, enum.Enum):
    """Тип проекта (Стартап, Стажировка, Научно-исследовательский)"""
    startup = 'startup'
    internship = 'internship'
    research = 'research'


class WorkFormat(str, enum.Enum):
    """Формат работы (полный день, удаленная работа, гибкий график)"""
    full_time = 'full_time'
    remote = 'remote'
    flexible = 'flexible'


class ProjectKind(str, enum.Enum):
    """Вид проекта (Цифровая академия, Передовая инженерная школа (ПИШ))"""
    digital_academy = 'digital_academy'
    pish = 'pish'


class ProjectsFilters(BaseModel):
    statuses: list[ProjectStatus] = Field(description='Статусы')
    types: list[ProjectType] = Field(description='Типы')
    work_formats: list[WorkFormat] = Field(description='Форматы работы')
    kinds: list[ProjectKind] = Field(description='Виды')
    companies: list[ValueSchema] = Field(description='Компании')
    roles: list[ValueSchema] = Field(description='Роли')
    subject_areas: list[ValueSchema] = Field(description='Предметная область')
    skills: list[ValueSchema] = Field(description='Навыки (Компетенции)')


@dataclass
class ProjectsQueryParams:
    query: str | None = Query(default=None, description='Поисковый запрос')
    status: list[ProjectStatus] | None = Query(default=None, description='Статусы')
    type: list[ProjectType] | None = Query(default=None, description='Тип')
    work_format: list[WorkFormat] | None = Query(default=None, description='Формат работы')
    kind: list[ProjectKind] | None = Query(default=None, description='Вид')

    duration_from: int | None = Query(default=None, description='Продолжительность от (дней)', ge=0)
    duration_to: int | None = Query(default=None, description='Продолжительность до (дней)', le=1000)

    company: list[int] | None = Query(default=None, description='Компания')
    role: list[int] | None = Query(default=None, description='Роль в проекте')
    subject_area: list[int] | None = Query(default=None, description='Предметная область')
    skills: list[int] | None = Query(default=None, description='Навыки (Компетенции)')


class Project(BaseModel):
    from companies.schemas import CompanyShort

    id: int
    name: str = Field(title='Название проекта')
    status: ProjectStatus | None = Field(title='Статус проекта')
    finish_date: datetime.date | None = Field(title='Дата завершения проекта')
    competences: list[ValueSchema] | None = Field(title='Компетенции, необходимые для проекта')

    duration: int = Field(ge=1, title='Продолжительность проекта в днях')
    type: ProjectType | None = Field(title='Тип проекта')
    kind: ProjectKind | None = Field(title='Вид проекта')
    company: CompanyShort = Field(title='Компания, которая разместила проект')


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
    work_load: str = Field(title='Загрузка')
    work_format: str = Field(title='Формат работы')
    needed_competencies: list[ValueSchema] = Field(title='Требуемые компетенции')
    acquired_competencies: list[ValueSchema] = Field(title='Компетенции, которые получит студент по итогам работы')


class ProjectDetails(Project):
    from companies.schemas import CompanyShort

    start_date: datetime.date = Field(title='Дата начала проекта')
    finish_date: datetime.date = Field(title='Дата завершения проекта')
    is_only_for_digital_academy: bool = Field(title='Проект доступен только для студентов цифровой академии')
    description: str = Field(title='Описание проекта')
    roles: list[ProjectRole] = Field(title='Роли')
    solving_problems: str = Field(title='Решаемые проблемы')
    goals: str = Field(title='Цели')
    tasks: str = Field(title='Задачи')
    results: str = Field(title='Результат')
    what_will_participant_get: str = Field(title='Что получит участник')
    stages: list[ProjectStage] = Field(title='Этапы и сроки проекта')
    companies: list[CompanyShort] = Field(title='Компании организаторы и партнёры')
    team: list[ProjectMember] = Field(title='Команда')
    other_projects: list[Project] = Field(title='Другие проекты этой области')

    is_applied: bool = Field(default=False, title='Признак того, что пользователь подал заявку на участие в проекте')
    attach_report_last_date: datetime.date | None = Field(title='Дата, до которой можно прикрепить отчёт')


class ParticipationCreate(BaseModel):
    role_id: int = Field(ge=1, title='Id роли')
    about: str = Field(title='О себе')
    competencies: str = Field(title='Компетенции и личные качества')
    experience: str = Field(title='Опыт')
