from typing import Any, Dict, Optional

from pydantic import BaseModel


class Request(BaseModel):
    request_id: str
    updated_at: Optional[str]
    request_metadata: Optional[Dict[str, Any]]
    status: str
