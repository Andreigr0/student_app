import datetime
import random

from faker import Faker
from fastapi import FastAPI

from app.database import setup_engine, setup_db
from app.models import *
from app.database import Base, get_settings
from projects.models import ProjectType, ProjectKind

app = FastAPI()

engine = setup_engine()
SessionLocal = setup_db(engine)
db = SessionLocal()

# seed CategoryModel table with random data
faker = Faker()


def seed_users():
    for i in range(20):
        user = UserModel(
            name=faker.word(),
            email=faker.email(),
            password='123',
            email_verified_at=faker.date_time(),
        )
        db.add(user)
    db.commit()


def seed_companies():
    for i in range(20):
        company = CompanyModel(
            name=faker.company(),
            description=faker.text(),
            has_accreditation=faker.boolean(),
            site=faker.url(),
        )
        db.add(company)


def seed_projects():
    for i in range(10000):
        status = random.choice(list(ProjectStatus))

        project = ProjectModel(
            name='Test project',
            status=random.choice(list(ProjectStatus)),
            start_date=datetime.date(2021, 1, 1),
            finish_date=datetime.date(2021, 2, 1),
            type=random.choice(list(ProjectType)),
            kind=random.choice(list(ProjectKind)),
            is_only_for_digital_academy=faker.boolean(),
            description=faker.text(),
            solving_problems=faker.text(),
            goals=faker.text(),
            tasks=faker.text(),
            results=faker.text(),
            what_will_participant_get=faker.text(),
        )
        from projects.models import ProjectsCompaniesModel, ProjectCompanyType

        association1 = ProjectsCompaniesModel(
            company_id=faker.random_int(min=1, max=20),
            type=ProjectCompanyType.organizer,
        )
        project.projects_companies.append(association1)

        db.add(project)


try:
    # seed_users()
    # seed_companies()
    seed_projects()
    db.commit()
except Exception as e:
    print(e)
