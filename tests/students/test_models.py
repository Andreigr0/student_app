from students.models import StudentModel


def test_create_student(db_test):
    student = StudentModel(
        about='About',
        resume='Resume',
        resume_content_type='application/pdf',
        resume_file_size=123,
        is_full_feedback=True,
    )
    db_test.add(student)
    db_test.commit()

    assert student.id is not None
    assert student.about == 'About'
    assert student.resume == 'Resume'
    assert student.resume_content_type == 'application/pdf'
    assert student.resume_file_size == 123
    assert student.is_full_feedback is True
