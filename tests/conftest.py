import datetime
import logging
import os
import pathlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.database import get_db


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
def monkey_session():
    from _pytest.monkeypatch import MonkeyPatch
    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@pytest.fixture(autouse=True, scope='session')
def get_settings(monkey_session):
    def _get_settings():
        return Settings(_env_file=f"{pathlib.Path(__file__).resolve().parent.parent}/test.env")

    monkey_session.setattr('app.database.get_settings', _get_settings)
    return _get_settings


class RawSQLFormatter(logging.Formatter):
    def format(self, record):
        if record.msg.startswith("SELECT") or record.msg.startswith("INSERT") or \
                record.msg.startswith("UPDATE") or record.msg.startswith("DELETE") or \
                record.msg.startswith("BEGIN") or record.msg.startswith("COMMIT") or \
                record.msg.startswith("ROLLBACK"):
            return record.getMessage() + '\n'
        return ''


class NoEmptyMessagesFilter(logging.Filter):
    def filter(self, record):
        if record.msg.startswith("SELECT") or record.msg.startswith("INSERT") or \
                record.msg.startswith("UPDATE") or record.msg.startswith("DELETE") or \
                record.msg.startswith("BEGIN") or record.msg.startswith("COMMIT") or \
                record.msg.startswith("ROLLBACK"):
            return True
        return False


@pytest.fixture(scope='session')
def testing_engine(monkey_session, get_settings):
    testing_engine = create_engine(get_settings().DATABASE_URI, echo=True, hide_parameters=False)

    def _testing_engine():
        return testing_engine

    monkey_session.setattr('app.database.setup_engine', _testing_engine)

    logger = logging.getLogger('sqlalchemy')
    logger.propagate = False

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RawSQLFormatter())
    logger.handlers = [handler]
    handler.addFilter(NoEmptyMessagesFilter())

    return testing_engine


@pytest.fixture(autouse=True)
def apply_migrations(monkey_session, get_settings):
    import alembic.config
    os.chdir(Path(__file__).parent.parent)
    alembic.config.main(argv=['upgrade', 'head'])
    yield
    alembic.config.main(argv=['downgrade', 'base'])


@pytest.fixture()
def get_db_override(testing_engine):
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)

    def _get_db() -> Session:
        db: Session = TestingSession()
        try:
            yield db
        finally:
            db.close()

    return _get_db


@pytest.fixture()
def db_test(get_db_override):
    yield from get_db_override()


@pytest.fixture()
def test_client(get_db_override, testing_engine, monkey_session):
    from app.main import app
    app.dependency_overrides[get_db] = get_db_override
    return TestClient(app)


@pytest.fixture()
def test_client_auth(get_db_override, testing_engine, monkey_session):
    from app.main import app
    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)

    auth = client.post('/users', data={'username': 'test@test.com', 'password': 'password'})
    client.headers = {'Authorization': f'Bearer {auth.json()["access_token"]}'}
    return client


@pytest.fixture()
def create_company(db_test, faker):
    from companies.models import CompanyModel

    def _create_company() -> CompanyModel:
        company = CompanyModel(
            name=faker.company(),
            description=faker.text(),
            has_accreditation=True,
        )
        db_test.add(company)
        db_test.commit()
        return company

    return _create_company


@pytest.fixture()
def create_student(db_test, faker):
    from students.models import StudentModel

    def _create_student() -> StudentModel:
        student = StudentModel(
            email=faker.email(),
            password="password",
            first_name='first_name',
            last_name='last_name',
            patronymic='patronymic',
            course='course',
            group='group',
            birthdate=datetime.date(2000, 1, 1),
            avatar='avatar',
            training_direction='training_direction',
            training_profile='training_profile',
            faculty='faculty',
            cathedra='cathedra',
            training_form='training_form',
            about='about',
            resume='resume',
            record_book_number='record_book_number',
            document_number='document_number',
            snils='snils',
        )
        db_test.add(student)
        db_test.commit()
        return student

    return _create_student


@pytest.fixture()
def create_company_representative(db_test, faker, create_company):
    from companies.models import CompanyRepresentativeModel

    def _create_company_representative() -> CompanyRepresentativeModel:
        company = create_company()
        company_representative = CompanyRepresentativeModel(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            birthdate=datetime.date(2000, 1, 1),
            email=faker.email(),
            password="password",
        )
        company_representative.company = company

        db_test.add(company_representative)
        db_test.commit()
        return company_representative

    return _create_company_representative


@pytest.fixture()
def create_project_model(db_test, create_company):
    from projects.models import ProjectModel, ProjectStatus, ProjectType, ProjectKind

    def _create_project_model(status: ProjectStatus | None = None, attach_company: bool = False) -> ProjectModel:
        project = ProjectModel(
            name='Test project',
            status=status or ProjectStatus.under_recruitment,
            start_date=datetime.date(2021, 1, 1),
            finish_date=datetime.date(2021, 2, 1),
            type=ProjectType.research,
            kind=ProjectKind.digital_academy,
            is_only_for_digital_academy=True,
            description='Test description',
            solving_problems='Test solving problems',
            goals='Test goals',
            tasks='Test tasks',
            results='Test results',
            what_will_participant_get='Test what will participant get',
        )
        if attach_company:
            company = create_company()
            from projects.models import ProjectsCompaniesModel, ProjectCompanyType
            association1 = ProjectsCompaniesModel(company=company, type=ProjectCompanyType.organizer)
            project.companies.append(association1)

        db_test.add(project)
        db_test.commit()
        return project

    return _create_project_model


@pytest.fixture
def create_project_role_model(db_test, create_project_model):
    from competencies.models import CompetencyModel
    from projects.models import ProjectRoleModel, WorkFormat

    def _create_project_role_model() -> ProjectRoleModel:
        project = create_project_model(attach_company=True)
        competency1, competency2 = CompetencyModel(name='Test competency 1'), CompetencyModel(name='Test competency 2')

        role = ProjectRoleModel(
            work_load='Test work load',
            work_format=WorkFormat.full_time,
        )
        role.project = project

        role.needed_competencies.append(competency1)
        role.needed_competencies.append(competency2)

        role.acquired_competencies.append(competency1)

        db_test.add(role)
        db_test.commit()

        assert role.project_id == project.id
        assert set(role.needed_competencies) == {competency1, competency2}
        assert set(role.acquired_competencies) == {competency1}

        return role

    return _create_project_role_model
