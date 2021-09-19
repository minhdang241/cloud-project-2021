from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from app.db.postgres import models
from .crud_base import CRUDBase
from sqlalchemy.orm import Session
from sqlalchemy import func

class CareerCreate(BaseModel):
    career_path: str
    skills: Optional[List[str]]
    total_jobs: Optional[int]


class CareerUpdate(BaseModel):
    skills: Optional[List[str]]
    total_jobs: Optional[int]


class CRUDCareer(CRUDBase[models.Career, CareerCreate, CareerUpdate]):
    def get_career_count(self, db: Session):
        return db.query(self.model).count()


career = CRUDCareer(models.Career)
