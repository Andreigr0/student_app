from typing import Type, Any

from fastapi import Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session, joinedload

from app.models import ProjectModel
from competencies.models import CompetencyModel
from projects.models import ProjectStatus, ProjectType, WorkFormat, ProjectKind, ProjectRoleModel, \
    ProjectsCompaniesModel, project_competencies
from projects.schemas import ProjectsQueryParams
from shared.schemas import PaginationQuery


def get_projects(db: Session, pagination: PaginationQuery, filters: ProjectsQueryParams):
    def is_list(obj: object, expected_type: Type[Any]) -> bool:
        return isinstance(obj, list) and all(isinstance(item, expected_type) for item in obj)

    query = db.query(ProjectModel)

    if isinstance(filters.query, str) and filters.query:
        query = query.filter(ProjectModel.name.ilike(f'%{filters.query}%'))

    if is_list(filters.statuses, ProjectStatus):
        query = query.filter(ProjectModel.status.in_(filters.statuses))

    if is_list(filters.types, ProjectType):
        query = query.filter(ProjectModel.type.in_(filters.types))

    if is_list(filters.work_formats, WorkFormat):
        query = query.filter(ProjectModel.roles.any(ProjectRoleModel.work_format.in_(filters.work_formats)))

    if is_list(filters.kinds, ProjectKind):
        query = query.filter(ProjectModel.kind.in_(filters.kinds))

    if isinstance(filters.duration_from, int):
        query = query.filter(ProjectModel.duration >= filters.duration_from)

    if isinstance(filters.duration_to, int):
        query = query.filter(ProjectModel.duration <= filters.duration_to)

    if is_list(filters.company, int):
        query = query.join(ProjectsCompaniesModel).filter(ProjectsCompaniesModel.company_id.in_(filters.company))

    if is_list(filters.roles, int):
        query = query.filter(ProjectModel.roles.any(ProjectRoleModel.id.in_(filters.roles)))

    # if is_list(filters.subject_areas, int):
    #     query = query.filter(ProjectModel.subject_areas.any(id.in_(filters.subject_areas)))

    if is_list(filters.skills, int):
        query = query.join(project_competencies).join(CompetencyModel).filter(CompetencyModel.id.in_(filters.skills))

    query = query.order_by(ProjectModel.id.desc())

    if isinstance(pagination.page, int) and isinstance(pagination.per_page, int):
        offset = (pagination.page - 1) * pagination.per_page
        query = query.offset(offset).limit(pagination.per_page)

    return query.all()
