from sqlalchemy.orm import Session

from app.exceptions import ModelNotFoundException
from companies.models import CompanyModel
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
