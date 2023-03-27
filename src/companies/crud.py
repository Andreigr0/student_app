from sqlalchemy.orm import Session

from app.exceptions import ModelNotFoundException
from app.models import CompanyModel
from shared.schemas import PaginationQuery


def get_companies(db: Session, pagination: PaginationQuery):
    query = db.query(CompanyModel)

    offset = (pagination.page - 1) * pagination.per_page
    query = query.offset(offset).limit(pagination.per_page)

    return query.all()


def get_company(db: Session, company_id: int):
    company = db.query(CompanyModel).get(company_id)
    if not company:
        raise ModelNotFoundException(CompanyModel)
    return company


def get_company_projects(db: Session, company_id: int):
    company = get_company(db=db, company_id=company_id)
    return company.organized_projects.all()
