import pytest


@pytest.mark.anyio
async def test_get_companies(test_client, create_company):
    create_company()
    create_company()
    create_company()

    response = test_client.get('/companies?page=2&per_page=2')

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_get_company(test_client, create_company):
    create_company()

    response = test_client.get('/companies/1')

    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.anyio
async def test_get_company_not_found(test_client):
    response = test_client.get('/companies/1')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Company not found'}

