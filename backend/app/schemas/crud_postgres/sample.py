from typing import Optional, Union

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class SampleCreate(BaseModel):
    request_name: str
    schedule: Union[str, None]
    user_id: str
    request_metadata: dict


class SampleUpdate(BaseModel):
    created_success: Optional[bool] = None
    request_metadata: Optional[dict] = None
