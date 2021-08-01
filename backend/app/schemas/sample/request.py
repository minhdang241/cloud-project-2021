"""
File contains API request body data model
"""
from pydantic import BaseModel


class SampleDTO(BaseModel):
    user_input: str
