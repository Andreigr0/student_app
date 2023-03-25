import datetime
import enum
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field

from shared.schemas import ValueSchema


class InvitationStatus(str, enum.Enum):
    """Статус приглашения (Новое, Просмотрено, Согласие, В команде, Отклонено, Отозвано, Просрочено)"""

    latest = 'latest'
    viewed = 'viewed'
    consent = 'consent'
    in_team = 'in_team'
    rejected = 'rejected'
    revoked = 'revoked'
    expired = 'expired'


class InvitationsCategory(str, enum.Enum):
    """Категория приглашений"""

    active = 'active'
    archived = 'archived'


@dataclass
class InvitationsQueryParams:
    category: InvitationsCategory | None = Query(default=None, description='Категория')
    status: list[InvitationStatus] | None = Query(default=None, description='Статусы')
    project_role: list[int] | None = Query(default=None, description='Роль в проекте')
    company: list[int] | None = Query(default=None, description='Компания')


class InvitationsFilters(BaseModel):
    statuses: list[InvitationStatus] = Field(description='Статусы')
    project_roles: list[ValueSchema] = Field(description='Роли в проектах')
    companies: list[ValueSchema] = Field(description='Компании')


class RepresentativeContacts(BaseModel):
    """Контакты представителя"""

    full_name: str = Field(description='ФИО')
    position: str = Field(description='Должность')
    telegram: str | None = Field(description='Telegram')
    email: str | None = Field(description='Email')
    phone: str | None = Field(description='Телефон')


class Invitation(BaseModel):
    from companies.schemas import CompanyShort

    id: int
    status: InvitationStatus = Field(description='Статус')
    date: datetime.date = Field(description='Дата')
    project_role: str = Field(description='Роль в проекте')
    project_title: str = Field(description='Название проекта')
    company: CompanyShort = Field(description='Компания')


class InvitationDetails(Invitation):
    from projects.schemas import Project

    contact: RepresentativeContacts = Field(description='Контакты представителя')
    invitation: str = Field(description='Текст приглашения')
    project: Project = Field(description='Проект, к которому относится приглашение')
    project_description: str = Field(description='Описание проекта')
    work_load: str = Field(description='Загрузка')
    work_format: str = Field(description='Формат работы')
    needed_skills: list[ValueSchema] = Field(description='Требуемые компетенции')
    acquired_skills: list[ValueSchema] = Field(description='Компетенции, которые получит участник')
    benefits: str = Field(description='Что получит участник')
