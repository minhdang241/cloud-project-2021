from typing import List

from pydantic import BaseModel


class WordFreq(BaseModel):
    value: str
    count: int


class WordFrequencies(BaseModel):
    words: List[WordFreq]


class Counts(BaseModel):
    course_count: int
    job_count: int
    company_count: int
    career_count: int
