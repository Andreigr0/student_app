def test_create_company_model(create_company):
    company = create_company()

    assert company.id == 1
    assert company.name is not None
    assert company.description is not None
    assert company.has_accreditation is True


def test_create_company_representative(db_test, create_company_representative):
    company_representative = create_company_representative()

    assert company_representative.id == 1
    assert company_representative.first_name is not None
    assert company_representative.last_name is not None
    assert company_representative.birthdate is not None
    assert company_representative.email is not None
