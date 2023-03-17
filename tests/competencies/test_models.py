from competencies.models import CompetenceModel


def test_create_competence(db_test, faker):
    competence = CompetenceModel(name=faker.word())
    db_test.add(competence)
    db_test.commit()
    assert competence.id is not None
    assert competence.name is not None
