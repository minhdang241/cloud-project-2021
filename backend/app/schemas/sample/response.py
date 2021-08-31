"""
File contains API response
"""
from typing import List, Optional

from pydantic import BaseModel


class CourseDTO(BaseModel):
    id: int
    code: Optional[str]
    title: Optional[str]
    description: Optional[str]
    outcome: Optional[str]
    level: Optional[str]

    class Config:
        orm_mode = True
        extra = "ignore"


class SchoolDTO(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        extra = "ignore"


class JobDTO(BaseModel):
    id: int
    title: Optional[str]
    company_name: Optional[str]
    company_location: Optional[str]
    short_description: Optional[str]
    description: Optional[str]
    link: Optional[str]
    career: Optional[str]

    class Config:
        orm_mode = True
        extra = "ignore"