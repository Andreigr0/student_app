from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from companies.models import CompanyModel
from companies.schemas import Company, CompanyDetails
from projects.schemas import Project

router = APIRouter(
    prefix='/companies',
    tags=['companies'],
)


@router.get('', response_model=list[Company])
# @router.get('')
def get_companies(db: Session = Depends(get_db)):
    return db.query(CompanyModel).all()


@router.get('/{id}')
def get_company(id: int, db: Session = Depends(get_db)) -> CompanyDetails:
    return db.query(CompanyModel).get(id)


@router.get('/{id}/projects', response_model=list[Project])
def get_company_projects(id: int, db: Session = Depends(get_db)):
    return db.query(CompanyModel).get(id).projects


@router.post('/{id}/subscribe', summary='Подписаться на компанию', status_code=201)
def subscribe_to_company(id: int, db: Session = Depends(get_db)):
    # return db.query(CompanyModel).get(id).projects
    pass
