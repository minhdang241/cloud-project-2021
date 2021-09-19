from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, asc

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

    def get_job_company_count(self, db: Session):
        return db.query(self.model.company_name, func.count(self.model.company_name).label("count")).group_by(self.model.company_name).all()

    def get_job_district_count(self, db: Session):
        return db.query(self.model.company_district, func.count(self.model.company_district).label("count")).group_by(self.model.company_district).all()


job = CRUDJob(models.Job)
