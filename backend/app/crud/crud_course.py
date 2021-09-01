from typing import Optional

from pydantic import BaseModel

from app.db.postgres import models
from .crud_base import CRUDBase


class CourseCreate(BaseModel):
    school_id: int
    code: str
    title: str
    description: str
    outcome: str
    level: str
    skills: Optional[str]
    embeddings: Optional[str]


class CourseUpdate(BaseModel):
    school_id: int
    code: str
    title: str
    description: str
    outcome: str
    level: str
    skills: Optional[str]
    embeddings: Optional[str]


class CRUDCourse(CRUDBase[models.Course, CourseCreate, CourseUpdate]):
    pass


course = CRUDCourse(models.Course)
