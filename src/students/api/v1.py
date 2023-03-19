from fastapi import APIRouter
from pydantic import Field

from app.tags import Tags
from projects.schemas import Project
from reviews.schemas import Review
from students.schemas import StudentCompetencies, StudentPortfolio, PublicStudent, PersonalStudent, \
    UpdateStudentCompetencies

current_router = APIRouter(
    prefix='/student',
    tags=[Tags.student],
)
public_router = APIRouter(
    prefix='/students',
    tags=[Tags.students],
)


@current_router.get('', summary='Личный профиль студента')
def get_current_student() -> PersonalStudent:
    pass


@current_router.get('/competencies')
def get_current_student_competencies() -> StudentCompetencies:
    pass


@current_router.patch('/competencies')
def update_current_student_competencies(body: UpdateStudentCompetencies) -> StudentCompetencies:
    pass


@current_router.get('/portfolio')
def get_current_student_portfolio() -> StudentPortfolio:
    pass


@current_router.get('/projects')
def get_current_student_projects() -> list[Project]:
    pass


@current_router.get('/reviews')
def get_current_student_reviews() -> list[Review]:
    pass


@public_router.get('/{id}', summary='Публичный профиль студента')
def get_public_student(id: int) -> PublicStudent:
    pass


@public_router.get('/{id}/competencies')
def get_student_competencies(id: int) -> StudentCompetencies:
    pass


@public_router.get('/{id}/portfolio')
def get_student_portfolio(id: int) -> StudentPortfolio:
    pass


@public_router.get('/{id}/projects')
def get_student_projects(id: int) -> list[Project]:
    pass


@public_router.get('/{id}/reviews')
def get_student_reviews(id: int) -> list[Review]:
    pass
