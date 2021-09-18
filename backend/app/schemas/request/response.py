from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Extra
import datetime

class Request(BaseModel):
    id: str
    created_at: Union[str, Any]
    updated_at: Optional[datetime.datetime]
    request_metadata: Optional[Dict[str, Any]]
    status: str

    class Config:
        extra = Extra.ignore
        orm_mode = True
