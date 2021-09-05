from typing import List, Optional

from pydantic import BaseModel


#
class Job(BaseModel):
    title: str
    company_name: str
    company_location: str
    short_description: Optional[str]
    link: str

    class Config:
        extra = "ignore"


class Career(BaseModel):
    career: str
    job_list: List[Job]

    class Config:
        extra = "ignore"


class CareerRecommendationResponse(BaseModel):
    career_list: List[Career]

    class Config:
        extra = "ignore"


# Response schema for Mismatch skills api
class Course(BaseModel):
    name: str
    link: str
    source: str


class Skill(BaseModel):
    name: str
    recommended_courses: List[Optional[Course]] = []


class MismatchSkillsRecommendationResponse(BaseModel):
    missing_skills: List[Skill] = []
    matching_skills: List[Skill] = []

    class Config:
        extra = "ignore"
