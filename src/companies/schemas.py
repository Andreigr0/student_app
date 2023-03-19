from typing import Any

from pydantic import BaseModel

from shared.schemas import ValueSchema


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

    # status: str
    # reason_rejection: str
    # contacts: list[Contact]
    # subscribers: list[CompaniesSubscribers]
    # type_activities: list[CompanyTypeActivities]
    projects: list[Project]

    class Config:
        orm_mode = True
