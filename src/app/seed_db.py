from faker import Faker
from fastapi import FastAPI

from app.database import setup_engine, setup_db
from app.models import *
from app.database import Base, get_settings

app = FastAPI()

engine = setup_engine()
SessionLocal = setup_db(engine)
db = SessionLocal()

# seed CategoryModel table with random data
fake = Faker()

try:
    db.commit()
except Exception as e:
    print(e)
