from companies.models import CompanyModel, CompanyEmployeeCount, CompanyStatus


def test_create_model(db_test, faker):
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

    assert company.id is not None
    assert company.name == 'Company 1'
    assert company.email == 'email@email.com'
    assert company.has_accreditation is True
    assert company.employee_count == CompanyEmployeeCount.small
    assert company.status == CompanyStatus.moderation
