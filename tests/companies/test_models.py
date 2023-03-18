from companies.models import CompanyModel, CompanyEmployeeCount, CompanyStatus, ContactModel, ContactCommunicationType, \
    CompaniesSubscribersModel, TypeActivityModel
from students.models import StudentModel


def test_create_company_model(create_company_model):
    company = create_company_model()

    assert company.id is not None
    assert company.name == 'Company 1'
    assert company.email == 'email@email.com'
    assert company.has_accreditation is True
    assert company.employee_count == CompanyEmployeeCount.small
    assert company.status == CompanyStatus.moderation


def test_create_contact_model(db_test, faker, create_company_model):
    company = create_company_model()

    contact = ContactModel(
        fio='FIO',
        email='email@email.com',
        position='position',
        telegram='telegram',
        phone='phone',
        communication_type=ContactCommunicationType.phone,
    )
    contact.company = company
    db_test.add(contact)
    db_test.commit()

    assert contact.id is not None
    assert contact.fio == 'FIO'
    assert contact.email == 'email@email.com'
    assert contact.position == 'position'
    assert contact.telegram == 'telegram'
    assert contact.phone == 'phone'
    assert contact.communication_type == ContactCommunicationType.phone
    assert contact.company_id == company.id


def test_create_subscription(db_test, create_company_model):
    company = create_company_model()

    student = StudentModel(
        about='About',
        resume='Resume',
        resume_content_type='application/pdf',
        resume_file_size=123,
        is_full_feedback=True,
    )

    company_subscription = CompaniesSubscribersModel();
    company_subscription.company = company
    student.subscribed_companies.append(company_subscription)

    db_test.add(student)
    db_test.commit()

    assert student.id is not None
    assert student.about == 'About'
    assert student.resume == 'Resume'
    assert student.resume_content_type == 'application/pdf'
    assert student.resume_file_size == 123
    assert student.is_full_feedback is True

    assert len(student.subscribed_companies) == 1
    assert student.subscribed_companies[0].company == company


def test_create_type_activity(db_test, faker):
    type_activity = TypeActivityModel(
        name='Name',
    )

    db_test.add(type_activity)
    db_test.commit()

    assert type_activity.id is not None
    assert type_activity.name == 'Name'
