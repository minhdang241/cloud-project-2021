from pydantic import BaseModel  # pylint: disable=no-name-in-module

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
    pass


job = CRUDJob(models.Job)
