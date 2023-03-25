from users.models import UserModel


def test_create_student(create_student):
    student = create_student()

    assert student.id == 1
    assert student.first_name is not None
    assert student.last_name is not None
    assert student.birthdate is not None
    assert student.email is not None


def test_create_company_representative(db_test, create_company_representative):
    company_representative = create_company_representative()

    assert company_representative.id == 1
    assert company_representative.first_name is not None
    assert company_representative.last_name is not None
    assert company_representative.birthdate is not None
    assert company_representative.email is not None


def test_created_users(db_test, create_student, create_company_representative):
    student = create_student()
    company_representative = create_company_representative()

    assert student.id == 1
    assert company_representative.id == 2
    assert db_test.query(UserModel).all() == [student, company_representative]
