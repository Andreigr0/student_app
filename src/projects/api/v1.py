from fastapi import APIRouter

from app.tags import Tags
from projects.schemas import Project, ProjectDetails, ParticipationCreate

router = APIRouter(
    prefix='/projects',
    tags=[Tags.projects],
)


@router.get('', response_model=list[Project])
def get_projects():
    return []


@router.get('/{id}')
def get_project(id: int) -> ProjectDetails:
    return None


@router.post('/{id}/participate', status_code=201, summary='Запрос на участие в проекте')
def participate_in_project(id: int, data: ParticipationCreate) -> ProjectDetails:
    pass
