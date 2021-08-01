"""
File contains API response
"""
from typing import List

from pydantic import BaseModel


class SampleDTO(BaseModel):
    resource_id: int
    url: str
    sample_list: List[int]
