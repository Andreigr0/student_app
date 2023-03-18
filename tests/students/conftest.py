import pytest

from students.models import StudentModel


@pytest.fixture
def create_student_model(db_test):
    def _create_student():
        student = StudentModel(
            about='About',
            resume='Resume',
            resume_content_type='application/pdf',
            resume_file_size=123,
            is_full_feedback=True,
        )
        db_test.add(student)
        db_test.commit()
        return student

    return _create_student
