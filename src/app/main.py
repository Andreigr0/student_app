import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

from app.database import setup_db, setup_engine

from companies.api import v1 as companies
from projects.api import v1 as projects
from students.api import v1 as students

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount('/files', StaticFiles(directory='files'), name='static')
app.include_router(companies.router)
app.include_router(projects.router)
app.include_router(students.current_router)
app.include_router(students.public_router)

engine = setup_engine()
SessionLocal = setup_db(engine)
