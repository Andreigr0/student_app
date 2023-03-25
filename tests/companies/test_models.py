def test_create_company_model(create_company):
    company = create_company()

    assert company.id == 1
    assert company.name is not None
    assert company.description is not None
    assert company.has_accreditation is True
