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
from users.models import UserModel

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
    from users.models import StudentModel

    def _create_student() -> StudentModel:
        student = StudentModel(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            birthdate=faker.date_of_birth(),
            email=faker.email(),
            password="password",
        )
        db_test.add(student)
        db_test.commit()
        return student

    return _create_student


@pytest.fixture()
def create_company_representative(db_test, faker, create_company):
    from users.models import CompanyRepresentativeModel

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
