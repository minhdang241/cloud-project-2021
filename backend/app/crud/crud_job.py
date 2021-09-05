from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sqlalchemy.orm import Session, joinedload

from app.db.postgres import models
from .crud_base import CRUDBase


class JobCreate(BaseModel):
    title: str
    company_name: str
    company_location: str
    short_description: str
    description: str
    link: str
    career: str
    skills: str


class JobUpdate(BaseModel):
    title: str
    company_name: str
    company_location: str
    short_description: str
    description: str
    link: str
    career: str
    skills: str


class CRUDJob(CRUDBase[models.Job, JobCreate, JobUpdate]):
    def get_job_with_career(self, db: Session):
        return db.query(self.model).options(joinedload("career")).all()


job = CRUDJob(models.Job)
