import pytest

from companies.models import CompanyModel, CompanyEmployeeCount, CompanyStatus


@pytest.fixture
def create_company_model(db_test, faker):
    def _create() -> CompanyModel:
        company = CompanyModel(
            name='Company 1',
            email='email@email.com',
            has_accreditation=True,
            site=faker.url(),
            description=faker.text(),
            logo=faker.url(),
            inn=faker.random_int(),
            employee_count=CompanyEmployeeCount.small,
            status=CompanyStatus.moderation,
            reason_rejection=faker.text(),
        )
        db_test.add(company)
        db_test.commit()
        return company

    return _create
