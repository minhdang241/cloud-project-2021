import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from app.api.api import router
from app.api.errors.handlers import (
    entity_error_handler,
    http_error_handler,
    validation_exception_handler,
    request_validation_exception_handler
)
from app.core.config import settings
from app.db.errors import EntityDoesNotExist

logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        Backend codebase
        """,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    application.add_exception_handler(ValidationError, validation_exception_handler)
    application.add_exception_handler(EntityDoesNotExist, entity_error_handler)

    application.include_router(router, prefix=settings.API_PREFIX)
    return application


app = get_application()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
