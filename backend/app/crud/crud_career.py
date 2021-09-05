from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from app.db.postgres import models
from .crud_base import CRUDBase


class CareerCreate(BaseModel):
    career_path: str
    skills: Optional[List[str]]
    total_jobs: Optional[int]


class CareerUpdate(BaseModel):
    skills: Optional[List[str]]
    total_jobs: Optional[int]


class CRUDCareer(CRUDBase[models.Career, CareerCreate, CareerUpdate]):
    pass


career = CRUDCareer(models.Career)
