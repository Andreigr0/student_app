from competencies.models import CompetencyModel, SubjectAreaModel


def test_create_competence(db_test, faker):
    competence = CompetencyModel(name=faker.word())
    db_test.add(competence)
    db_test.commit()
    assert competence.id is not None
    assert competence.name is not None


def test_create_subject_area_model(db_test, faker):
    subject_area = SubjectAreaModel(name='name')
    db_test.add(subject_area)
    db_test.commit()

    assert subject_area.id is not None
    assert subject_area.name == 'name'
