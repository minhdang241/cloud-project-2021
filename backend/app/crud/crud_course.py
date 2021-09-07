from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func


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
    def get_course_level_count(self, db: Session):
        return db.query(self.model.level, func.count(self.model.level).label("count")).group_by(self.model.level).all()


course = CRUDCourse(models.Course)
