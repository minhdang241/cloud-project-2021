from typing import Any, Dict, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from app.db.postgres import models
from .crud_base import CRUDBase


class RequestCreate(BaseModel):
    status: str
    created_success: bool


class RequestUpdate(BaseModel):
    status: str
    updated_at: str
    request_metadata: Optional[Dict[str, Any]]


class CRUDCareer(CRUDBase[models.Request, RequestCreate, RequestUpdate]):
    pass


request = CRUDCareer(models.Request)
