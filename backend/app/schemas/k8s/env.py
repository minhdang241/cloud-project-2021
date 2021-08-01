from pydantic import BaseModel

from app.core.config import settings


class SampleEnvironment(BaseModel):
    """
    list all env that job needs
    """
    BACKEND_ADDRESS: str = settings.BACKEND_ADDRESS
