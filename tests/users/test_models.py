from users.models import UserModel


def test_created_users(db_test, create_student, create_company_representative):
    student = create_student()
    company_representative = create_company_representative()

    assert student.id == 1
    assert company_representative.id == 2
    assert db_test.query(UserModel).all() == [student, company_representative]
