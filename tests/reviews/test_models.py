import datetime

from reviews.models import ReviewModel


def test_create_review(db_test, create_student, create_project_role_model):
    student = create_student()
    project_role = create_project_role_model()

    review = ReviewModel(
        student=student,
        role=project_role,
        score=5,
        text='text',
        spent_hours=100,
        start_date=datetime.date(2020, 1, 1),
        finish_date=datetime.date(2020, 2, 1),
    )
    db_test.add(review)
    db_test.commit()

    assert review.student_id == 1
    assert review.role_id == 1
    assert review.score == 5
    assert review.text == 'text'
    assert review.spent_hours == 100
    assert review.start_date == datetime.date(2020, 1, 1)
    assert review.finish_date == datetime.date(2020, 2, 1)
    assert review.project == project_role.project
    assert review.company is not None
