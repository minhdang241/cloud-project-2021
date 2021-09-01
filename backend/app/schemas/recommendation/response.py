from typing import List, Optional

from pydantic import BaseModel


class Job(BaseModel):
    title: str
    company_name: str
    company_location: str
    short_description: Optional[str]
    link: str

    class Config:
        orm_mode = True
        extra = "ignore"


class Career(BaseModel):
    career: str
    job_list: List[Job]

    class Config:
        orm_mode = True
        extra = "ignore"


class CareerRecommendationResponse(BaseModel):
    career_list: List[Career]

    class Config:
        orm_mode = True
        extra = "ignore"
