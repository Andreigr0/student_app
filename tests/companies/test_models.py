from companies.models import CompanyModel, CompanyEmployeeCount, CompanyStatus, ContactModel, ContactCommunicationType


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
