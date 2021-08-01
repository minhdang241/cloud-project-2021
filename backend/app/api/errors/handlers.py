from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST

from app.db.errors import EntityDoesNotExist


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {"status_code": exc.status_code, "errors": [exc.detail]}, status_code=exc.status_code
    )


async def entity_error_handler(_: Request, exc: EntityDoesNotExist) -> JSONResponse:
    return JSONResponse(
        {"status_code": HTTP_404_NOT_FOUND, "errors": [exc.detail]}, status_code=HTTP_404_NOT_FOUND
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


async def run_time_exception_handler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
