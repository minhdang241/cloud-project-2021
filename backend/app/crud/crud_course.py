from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc

from app.resources.utils import get_keyword_query
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

    def get_courses(
            self, db: Session, paging_params: Params = None, order_asc=True, sorted_by: str = None,
            level: str = None, title: str = None
    ):
        query = db.query(self.model)
        if level:
            query = query.filter(self.model.level == level.upper())
        if title:
            query = query.filter(self.model.title.ilike(get_keyword_query(title)))
        sorted_attr = getattr(self.model, sorted_by) if sorted_by and hasattr(self.model, sorted_by) else self.model.id
        if not order_asc:
            query = query.order_by(desc(sorted_attr))
        else:
            query = query.order_by(asc(sorted_attr))
        return paginate(query, paging_params) if paging_params else query.first()


course = CRUDCourse(models.Course)
