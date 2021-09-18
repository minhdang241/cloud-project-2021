import datetime

from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, TIMESTAMP)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from .setup_postgres import Base
from .type import career_type, course_level_type, request_status


class School(Base):
    name = Column(String)
    courses = relationship("Course", back_populates="school")


class Course(Base):
    id = Column('course_id', Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey(
        "Schools.school_id", ondelete="SET NULL"))
    code = Column(String)
    title = Column(String)
    description = Column(String)
    preprocessed_description = Column(String)
    outcome = Column(String)
    level = Column(course_level_type)
    skills = Column("skills", mutable_json_type(dbtype=JSONB, nested=True))
    embeddings = Column("embeddings", mutable_json_type(dbtype=JSONB, nested=True))
    school = relationship("School", back_populates="courses")


class Job(Base):
    title = Column(String)
    company_name = Column(String)
    company_location = Column(String)
    company_district = Column(String)
    short_description = Column(String)
    description = Column(String)
    link = Column(String, unique=True)
    skills = Column("skills", mutable_json_type(dbtype=JSONB, nested=True))
    embeddings = Column("embeddings", mutable_json_type(dbtype=JSONB, nested=True))
    career_id = Column(Integer, ForeignKey("Careers.career_id"))
    career = Column(career_type)
    preprocessed_description = Column(String)


class Career(Base):
    career_path = Column(career_type)
    skills = Column("skills", mutable_json_type(dbtype=JSONB, nested=True))
    total_jobs = Column(Integer)
    jobs = relationship("Job", cascade="delete", backref="job_career")
    embeddings = Column("embeddings", mutable_json_type(dbtype=JSONB, nested=True))


class Request(Base):
    status = Column(request_status)
    created_at = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    updated_at = Column(TIMESTAMP(timezone=True))
    created_success = Column(Boolean)
    request_metadata = Column("request_metadata", mutable_json_type(dbtype=JSONB, nested=True))
