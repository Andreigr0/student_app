from fastapi import APIRouter, Depends

from app.tags import Tags
from projects.schemas import Project, ProjectDetails, ParticipationCreate, ProjectsQueryParams, ProjectsFilters
from reports.schemas import Report

router = APIRouter(
    prefix='/projects',
    tags=[Tags.projects],
)


@router.get('/filters', summary='Получить доступные фильтры для проектов')
def get_projects_filters() -> ProjectsFilters:
    pass


@router.get('')
def get_projects(filters: ProjectsQueryParams = Depends()) -> list[Project]:
    return []


@router.get('/{id}')
def get_project(id: int) -> ProjectDetails:
    pass


@router.post('/{id}/apply', summary='Запрос на участие в проекте', tags=[Tags.invitations], status_code=201)
def participate_in_project(id: int, data: ParticipationCreate) -> ProjectDetails:
    pass


@router.get('/{id}/reports', tags=[Tags.reports], summary='Получить отчеты по проекту')
def get_project_reports(id: int) -> list[Report]:
    pass
