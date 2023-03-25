from competencies.models import CompetencyModel


def test_create_company_model(create_company, db_test):
    company = create_company()
    competency1, competency2 = CompetencyModel(name='test1'), CompetencyModel(name='test2')
    company.competencies.append(competency1)
    company.competencies.append(competency2)

    assert company.id == 1
    assert company.name is not None
    assert company.description is not None
    assert company.has_accreditation is True
    assert company.logo is None
    assert set(company.competencies) == {competency1, competency2}


def test_create_company_representative(db_test, create_company_representative):
    company_representative = create_company_representative()

    assert company_representative.id == 1
    assert company_representative.first_name is not None
    assert company_representative.last_name is not None
    assert company_representative.birthdate is not None
    assert company_representative.email is not None
