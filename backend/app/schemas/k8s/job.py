from typing import Optional

from pydantic import BaseModel


class SampleJob(BaseModel):
    container_name: Optional[str] = "sample-container"
    job_name: Optional[str] = "sample-job"
    job_id: str
