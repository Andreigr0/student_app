import random

from faker import Faker
from fastapi import FastAPI

from app.database import setup_engine, setup_db
from app.models import *
from app.database import Base, get_settings
from companies.models import CompanyEmployeeCount, CompanyStatus
from projects.models import ProjectTypeEnum, ProjectView, ProjectStatusEnum

app = FastAPI()

engine = setup_engine()
SessionLocal = setup_db(engine)
db = SessionLocal()

# seed CategoryModel table with random data
fake = Faker()


def seed_users():
    for i in range(20):
        user = UserModel(
            name=fake.word(),
            email=fake.email(),
            password='123',
            email_verified_at=fake.date_time(),
        )
        db.add(user)
    db.commit()


def seed_companies():
    for i in range(20):
        company = CompanyModel(
            email=fake.email(),
            name=fake.word(),
            inn=fake.pyint(),
            has_accreditation=fake.boolean(),
            site=fake.url(),
            logo=fake.url(),
            description=fake.text(),
            employee_count=random.choice(list(CompanyEmployeeCount)),
            status=random.choice(list(CompanyStatus)),
            reason_rejection=fake.text(),
            active_project_count=fake.pyint(),
        )
        db.add(company)


def seed_projects():
    for i in range(20):
        project = ProjectModel(
            company_id=fake.random_int(min=2, max=20),
            name=fake.word(),
            is_visible=fake.boolean(),
            type=random.choice(list(ProjectTypeEnum)),
            view=random.choice(list(ProjectView)),
            status=random.choice(list(ProjectStatusEnum)),
            description=fake.text(),
            problem=fake.text(),
            purpose=fake.text(),
            task=fake.text(),
            result=fake.text(),
            what_will_get=fake.text(),
            total=fake.text(),
            report=fake.text(),
            reason_rejection=fake.text(),
            application_date=fake.date_time(),
        )
        db.add(project)


try:
    # seed_users()
    # seed_companies()
    seed_projects()
    db.commit()
except Exception as e:
    print(e)
