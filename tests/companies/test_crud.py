from app.exceptions import ModelNotFoundException
from companies import crud
from shared.schemas import PaginationQuery


def test_get_company_not_found(db_test):
    try:
        crud.get_company(db=db_test, company_id=1)
    except ModelNotFoundException as e:
        assert e.message == 'Company not found'


def test_get_company(db_test, create_company):
    create_company()
    company = crud.get_company(db=db_test, company_id=1)
    assert company.id == 1


def test_get_companies(db_test, create_company):
    create_company()
    create_company()
    create_company()
    companies = crud.get_companies(db=db_test, pagination=PaginationQuery(page=2, per_page=2))
    assert len(companies) == 1
