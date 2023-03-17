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
