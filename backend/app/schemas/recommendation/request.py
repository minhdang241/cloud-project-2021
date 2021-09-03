from typing import List

from pydantic import BaseModel


class Course(BaseModel):
    course_id: int


class CareerRecommendationRequest(BaseModel):
    course_list: List[Course]
    topk: int = None