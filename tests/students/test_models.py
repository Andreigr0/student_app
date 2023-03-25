import datetime


def test_create_student(create_student):
    student = create_student()

    assert student.id == 1
    assert student.first_name == 'first_name'
    assert student.last_name == 'last_name'
    assert student.patronymic == 'patronymic'
    assert student.course == 'course'
    assert student.group == 'group'
    assert student.birthdate == datetime.date(2000, 1, 1)
    assert student.avatar == 'avatar'
    assert student.training_direction == 'training_direction'
    assert student.training_profile == 'training_profile'
    assert student.faculty == 'faculty'
    assert student.cathedra == 'cathedra'
    assert student.training_form == 'training_form'
    assert student.about == 'about'
    assert student.resume == 'resume'
    assert student.record_book_number == 'record_book_number'
    assert student.document_number == 'document_number'
    assert student.snils == 'snils'


def test_create_student_contact(db_test, create_student):
    from students.models import StudentContactModel

    student = create_student()
    student_contact = StudentContactModel(
        student=student,
        text='text',
    )
    db_test.add(student_contact)
    db_test.commit()

    assert student_contact.id == 1
    assert student_contact.student_id == 1
    assert student_contact.text == 'text'


def test_create_student_relative(db_test, create_student):
    from students.models import StudentRelativeModel

    student = create_student()
    student_relative = StudentRelativeModel(
        student=student,
        first_name='first_name',
        last_name='last_name',
        patronymic='patronymic',
        text='text',
    )
    db_test.add(student_relative)
    db_test.commit()

    assert student_relative.id == 1
    assert student_relative.student_id == 1
    assert student_relative.first_name == 'first_name'
    assert student_relative.last_name == 'last_name'
    assert student_relative.patronymic == 'patronymic'
    assert student_relative.text == 'text'


def test_create_student_competence(db_test, create_student):
    from competencies.models import CompetencyModel

    student = create_student()
    competence = CompetencyModel(name='name')
    student.competencies.append(competence)

    db_test.add(student)
    db_test.commit()

    assert student.competencies == [competence]


def test_create_student_subject_area(db_test, create_student):
    from competencies.models import SubjectAreaModel

    student = create_student()
    subject_area = SubjectAreaModel(name='name')
    student.subject_areas.append(subject_area)

    db_test.add(student)
    db_test.commit()

    assert student.subject_areas == [subject_area]
