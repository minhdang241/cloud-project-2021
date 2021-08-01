from pydantic import BaseModel


class Paging(BaseModel):
    total: int
    page: int
    size: int
