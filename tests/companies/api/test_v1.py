import pytest

from projects.models import ProjectStatus


@pytest.mark.anyio
async def test_get_companies(test_client, create_company):
    for _ in range(3):
        create_company()

    response = test_client.get('/companies?page=2&per_page=2')

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_get_company(test_client, create_company, create_project_model):
    company = create_company()
    for _ in range(5):
        status = ProjectStatus.recruited if _ % 2 == 0 else ProjectStatus.finished
        create_project_model(company=company, status=status)

    response = test_client.get('/companies/1')

    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert len(response.json()['projects']) == 3


@pytest.mark.anyio
async def test_get_company_not_found(test_client):
    response = test_client.get('/companies/1')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Company not found'}


@pytest.mark.anyio
async def test_ger_company_projects(test_client, create_company, create_project_model):
    company1, company2 = create_company(), create_company()

    for _ in range(10):
        create_project_model(company=company1)

    for _ in range(5):
        create_project_model(company=company2)

    response1 = test_client.get(f'/companies/{company1.id}/projects')
    response2 = test_client.get(f'/companies/{company2.id}/projects')

    assert response1.status_code == 200
    assert len(response1.json()) == 10
    assert len(response2.json()) == 5
