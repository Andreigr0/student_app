from fastapi import Request, FastAPI
from starlette.responses import JSONResponse

from app.exceptions import ModelNotFoundException


async def model_not_found_exception_handler(request: Request, exc: ModelNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(ModelNotFoundException, model_not_found_exception_handler)
