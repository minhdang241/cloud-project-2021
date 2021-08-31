from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship

from .setup_postgres import Base
from .type import course_level_type, career_type


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

    school = relationship("School", back_populates="courses")


class Job(Base):
    title = Column(String)
    company_name = Column(String)
    company_location = Column(String)
    short_description = Column(String)
    description = Column(String)
    link = Column(String)
    career = Column(career_type)
