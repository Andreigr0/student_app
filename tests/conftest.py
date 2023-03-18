import datetime
import logging
import os
import pathlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import get_db
from app.core.config import Settings
from companies.models import CompanyModel, CompanyEmployeeCount, CompanyStatus
from projects.models import ProjectModel, ProjectTypeEnum, ProjectView, ProjectStatusEnum

logger = logging.getLogger(__name__)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture()
def monkey_session():
    from _pytest.monkeypatch import MonkeyPatch
    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@pytest.fixture(autouse=True)
def get_settings(monkey_session):
    def _get_settings():
        return Settings(_env_file=f"{pathlib.Path(__file__).resolve().parent.parent}/test.env")

    monkey_session.setattr('app.database.get_settings', _get_settings)
    return _get_settings


@pytest.fixture()
def testing_engine(monkey_session, get_settings):
    testing_engine = create_engine(get_settings().DATABASE_URI)

    def _testing_engine():
        return testing_engine

    monkey_session.setattr('app.database.setup_engine', _testing_engine)
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


# @pytest.fixture()
# def create_user(db_test, faker):
#     def _create_user():
#         user_create = UserCreate(email=faker.email(), login=faker.user_name(), password='123')
#         from users import crud
#         user = crud.create_user(db=db_test, user=user_create)
#         return user
#
#     return _create_user


@pytest.fixture
def create_company_model(db_test, faker):
    def _create() -> CompanyModel:
        company = CompanyModel(
            name='Company 1',
            email=faker.email(),
            has_accreditation=True,
            site=faker.url(),
            description=faker.text(),
            logo=faker.url(),
            inn=faker.random_int(),
            employee_count=CompanyEmployeeCount.small,
            status=CompanyStatus.moderation,
            reason_rejection=faker.text(),
        )
        db_test.add(company)
        db_test.commit()
        return company

    return _create


@pytest.fixture
def create_project_model(db_test, faker, create_company_model):
    def _create() -> (ProjectModel, datetime.datetime):
        company = create_company_model()
        now = datetime.datetime.now()
        project = ProjectModel(
            name='test',
            is_visible=True,
            type=ProjectTypeEnum.Research,
            view=ProjectView.DigitalAcademy,
            status=ProjectStatusEnum.Done,
            description='description',
            problem='problem',
            purpose='purpose',
            task='task',
            result='result',
            what_will_get='what_will_get',
            total='total',
            report='report',
            reason_rejection='reason_rejection',
            application_date=now,
            company_id=company.id,
        )
        db_test.add(project)
        db_test.commit()
        return project, now

    return _create
