from typing import Any

from pydantic import BaseModel

from shared.schemas import ValueSchema
import enum


class CompanyEmployeeCount(enum.Enum):
    """Количество сотрудников в компании (Маленькая (до 20), Средняя (21-50), Большая (51-100), Огромная (>100))"""
    small = 'small'
    middle = 'middle'
    large = 'large'
    huge = 'huge'


class CompanyStatus(enum.Enum):
    """Статусы компании (Новая, Активна, На модерации, На удалении, Удалена, Заблокирована)"""
    new = 'new'
    active = 'active'
    moderation = 'moderation'
    deleting = 'deleting'
    deleted = 'deleted'
    blocked = 'blocked'


class ContactCommunicationType(str, enum.Enum):
    phone = "phone"
    email = "email"
    telegram = "telegram"


class CompanyShort(BaseModel):
    id: int
    name: str
    logo: str


class Company(CompanyShort):
    competencies: list[ValueSchema]
    has_accreditation: bool
    active_project_count: int
    total_project_count: int | None

    class Config:
        orm_mode = True


class CompanyDetails(Company):
    from projects.schemas import Project

    inn: int | None
    site: str
    description: str
    employee_count: Any
    projects: list[Project]

    class Config:
        orm_mode = True
