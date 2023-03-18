from competencies.models import SubjectAreaModel, CompetencyModel
from students.models import StudentsSubjectAreasModel, StudentsCompetenciesModel


def test_create_student(create_student_model):
    student = create_student_model()

    assert student.id is not None
    assert student.about == 'About'
    assert student.resume == 'Resume'
    assert student.resume_content_type == 'application/pdf'
    assert student.resume_file_size == 123
    assert student.is_full_feedback is True


def test_create_students_subject_areas(db_test, create_student_model):
    student = create_student_model()

    subject_area = SubjectAreaModel(name='Name')

    student_subject_area = StudentsSubjectAreasModel()
    student_subject_area.subject_area = subject_area
    student.subject_areas.append(student_subject_area)

    db_test.add(student)
    db_test.commit()

    assert student.id is not None
    assert len(student.subject_areas) == 1
    assert student.subject_areas[0].subject_area == subject_area


def test_create_students_competencies(db_test, create_student_model):
    student = create_student_model()

    competency = CompetencyModel(name='Name')

    students_competencies = StudentsCompetenciesModel()
    students_competencies.competency = competency
    student.competencies.append(students_competencies)

    db_test.add(student)
    db_test.commit()

    assert student.id is not None
    assert len(student.competencies) == 1
    assert student.competencies[0].competency == competency
