from fastapi import FastAPI

from academic_performance.api import v1 as academic_performance
from app.database import setup_db, setup_engine
from app.exception_handlers import setup_exception_handlers
from attendance.api import v1 as attendance
from companies.api import v1 as companies
from contacts.api import v1 as contacts
from curriculum.api import v1 as curriculum
from invitations.api import v1 as invitations
from projects.api import v1 as projects
from reports.api import v1 as reports
from reviews.api import v1 as reviews
from students.api import v1 as students

app = FastAPI(
    swagger_ui_parameters={  # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
        "docExpansion": "list",
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "filter": True,
    }
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount('/files', StaticFiles(directory='files'), name='static')
app.include_router(academic_performance.router)
app.include_router(attendance.router)
app.include_router(contacts.router)
app.include_router(companies.router)
app.include_router(projects.router)
app.include_router(students.current_router)
app.include_router(students.public_router)
app.include_router(curriculum.router)
app.include_router(reports.router)
app.include_router(invitations.router)
app.include_router(reviews.router)

engine = setup_engine()
SessionLocal = setup_db(engine)

setup_exception_handlers(app)
