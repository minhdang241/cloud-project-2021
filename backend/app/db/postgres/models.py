from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from .setup_postgres import Base
from .type import career_type, course_level_type


class School(Base):
    name = Column(String)
    courses = relationship("Course", back_populates="school")


class Course(Base):
    school_id = Column(Integer, ForeignKey(
        "Schools.school_id", ondelete="SET NULL"))
    code = Column(String)
    title = Column(String)
    description = Column(String)
    outcome = Column(String)
    level = Column(course_level_type)
    skills = Column("metrics", mutable_json_type(dbtype=JSONB, nested=True))
    school = relationship("School", back_populates="courses")


class Job(Base):
    title = Column(String)
    company_name = Column(String)
    company_location = Column(String)
    short_description = Column(String)
    description = Column(String)
    link = Column(String)
    career = Column(career_type)
