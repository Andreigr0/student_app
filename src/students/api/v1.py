from fastapi import APIRouter, Body, UploadFile
from pydantic import Field

from app.tags import Tags
from projects.schemas import Project
from reviews.schemas import Review
from shared.schemas import FileSchema
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


@current_router.patch('/about', summary='Обновить информацию о себе')
def update_current_student_about(about: str = Body(..., max_length=1000, title='О себе')):
    pass


@current_router.get('/resume', summary='Получить резюме')
def get_resume() -> FileSchema:
    pass


@current_router.post('/resume/generate', summary='Сгенерировать резюме')
def generate_resume() -> FileSchema:
    pass


@current_router.post('/resume/upload', summary='Загрузить резюме', status_code=201)
def upload_resume(file: UploadFile = Body(..., title='Файл')):
    pass


@current_router.delete('/resume', summary='Удалить резюме', status_code=204)
def delete_resume():
    pass


@current_router.get('/competencies/available',
                    summary='Получить доступные компетенции и предметные области',
                    tags=[Tags.competencies])
def get_available_competencies() -> StudentCompetencies:
    pass


@current_router.get('/competencies', summary='Получить компетенции текущего пользователя', tags=[Tags.competencies])
def get_current_student_competencies() -> StudentCompetencies:
    pass


@current_router.patch('/competencies', tags=[Tags.competencies], summary='Обновить компетенции текущего пользователя')
def update_current_student_competencies(body: UpdateStudentCompetencies) -> StudentCompetencies:
    pass


@current_router.get('/portfolio', tags=[Tags.portfolio])
def get_current_student_portfolio() -> StudentPortfolio:
    pass


@current_router.get('/projects', tags=[Tags.projects])
def get_current_student_projects() -> list[Project]:
    pass


@current_router.get('/reviews', tags=[Tags.reviews])
def get_current_student_reviews() -> list[Review]:
    pass


@public_router.get('/{id}', summary='Публичный профиль студента')
def get_public_student(id: int) -> PublicStudent:
    pass


@public_router.get('/{id}/competencies', tags=[Tags.competencies], summary='Получить компетенции студента')
def get_student_competencies(id: int) -> StudentCompetencies:
    pass


@public_router.get('/{id}/portfolio', tags=[Tags.portfolio])
def get_student_portfolio(id: int) -> StudentPortfolio:
    pass


@public_router.get('/{id}/projects', tags=[Tags.projects])
def get_student_projects(id: int) -> list[Project]:
    pass


@public_router.get('/{id}/reviews', tags=[Tags.reviews])
def get_student_reviews(id: int) -> list[Review]:
    pass
