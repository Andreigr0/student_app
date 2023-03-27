from app.exceptions import ModelNotFoundException
from companies import crud
from shared.schemas import PaginationQuery


def test_get_companies(db_test, create_company):
    create_company()
    create_company()
    create_company()
    companies = crud.get_companies(db=db_test, pagination=PaginationQuery(page=2, per_page=2))
    assert len(companies) == 1


def test_get_company_not_found(db_test):
    try:
        crud.get_company(db=db_test, company_id=1)
    except ModelNotFoundException as e:
        assert e.message == 'Company not found'


def test_get_company(db_test, create_company, create_project_model):
    company = create_company()
    for _ in range(5):
        create_project_model(company=company)

    company = crud.get_company(db=db_test, company_id=1)
    assert company.id == 1
    assert len(company.projects) == 3


def test_get_company_projects(db_test, create_company, create_project_model):
    company = create_company()
    for _ in range(10):
        create_project_model(company=company)

    projects = crud.get_company_projects(db=db_test, company_id=company.id)
    assert len(projects) == 10
