from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.tags import Tags
from companies.models import CompanyModel
from companies.schemas import Company, CompanyDetails
from projects.schemas import Project
from shared.schemas import PaginationQuery
from companies import crud

router = APIRouter(
    prefix='/companies',
    tags=[Tags.companies],
)


@router.get('', summary='Получить список компаний')
def get_companies(db: Session = Depends(get_db), pagination: PaginationQuery = Depends()) -> list[Company]:
    return crud.get_companies(db, pagination)


@router.get('/{id}')
def get_company(id: int, db: Session = Depends(get_db)) -> CompanyDetails:
    return crud.get_company(db, id)


@router.get('/{id}/projects', response_model=list[Project], tags=[Tags.projects, Tags.todo])
def get_company_projects(id: int, db: Session = Depends(get_db)):
    pass


@router.post('/{id}/subscribe', summary='Подписаться на компанию', status_code=201, tags=[Tags.todo])
def subscribe_to_company(id: int, db: Session = Depends(get_db)):
    pass
