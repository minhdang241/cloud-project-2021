from typing import List

from pydantic import BaseModel


class WordFreq(BaseModel):
    value: str
    count: int


class WordFrequencies(BaseModel):
    words: List[WordFreq]
