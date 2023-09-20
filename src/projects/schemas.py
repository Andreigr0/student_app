import datetime
import enum
from dataclasses import dataclass
from typing import Any

from fastapi import Query
from pydantic import BaseModel, Field

from shared.schemas import ValueSchema, CompanyShort
from projects.models import ProjectStatus, ProjectType, WorkFormat, ProjectKind, ProjectPosition, ProjectCompanyType


class ProjectsCategory(str, enum.Enum):
    """Категория проектов (Активные, Завершенные)"""
    active = 'active'
    finished = 'finished'


class CompanyParticipant(CompanyShort):
    type: ProjectCompanyType = Field(title='Роль компании в проекте')


class ProjectRole(BaseModel):
    id: int
    name: str
    work_load: str = Field(title='Загрузка')
    work_format: WorkFormat = Field(title='Формат работы')
    needed_competencies: list[ValueSchema] = Field(title='Требуемые компетенции')
    acquired_competencies: list[ValueSchema] = Field(title='Компетенции, которые получит студент по итогам работы')


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
    statuses: list[ProjectStatus] | None = Query(default=None, description='Статусы')
    types: list[ProjectType] | None = Query(default=None, description='Тип')
    work_formats: list[WorkFormat] | None = Query(default=None, description='Формат работы')
    kinds: list[ProjectKind] | None = Query(default=None, description='Вид')

    duration_from: int | None = Query(default=None, description='Продолжительность от (дней)', ge=0)
    duration_to: int | None = Query(default=None, description='Продолжительность до (дней)', le=1000)

    company: list[int] | None = Query(default=None, description='Компания')
    roles: list[int] | None = Query(default=None, description='Роль в проекте')
    subject_areas: list[int] | None = Query(default=None, description='Предметная область')
    skills: list[int] | None = Query(default=None, description='Навыки (Компетенции)')


class Project(BaseModel):
    id: int
    name: str = Field(title='Название проекта')
    status: ProjectStatus | None = Field(title='Статус проекта')
    start_date: datetime.date = Field(title='Дата начала проекта')
    finish_date: datetime.date = Field(title='Дата завершения проекта')
    duration: Any = Field(title='Продолжительность проекта (дней)') # todo fix
    competencies: list[ValueSchema] | None = Field(title='Компетенции, необходимые для проекта')

    type: ProjectType | None = Field(title='Тип проекта')
    kind: ProjectKind | None = Field(title='Вид проекта')
    company: CompanyShort | None = Field(title='Компания, которая разместила проект')

    class Config:
        orm_mode = True


class ProjectStage(BaseModel):
    id: int
    name: str
    start_date: datetime.date
    finish_date: datetime.date


class ProjectMember(BaseModel):
    id: int
    avatar: str | None
    name: str
    description: str
    position: ProjectPosition


class ProjectDetails(Project):
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
    companies: list[CompanyParticipant] = Field(title='Компании организаторы и партнёры')
    team: list[ProjectMember] = Field(title='Команда')
    other_projects: list[Project] = Field(title='Другие проекты этой области')

    is_applied: bool = Field(default=False, title='Признак того, что пользователь подал заявку на участие в проекте')
    attach_report_last_date: datetime.date | None = Field(title='Дата, до которой можно прикрепить отчёт')


class ParticipationCreate(BaseModel):
    role_id: int = Field(ge=1, title='Id роли')
    about: str = Field(title='О себе')
    competencies: str = Field(title='Компетенции и личные качества')
    experience: str = Field(title='Опыт')
