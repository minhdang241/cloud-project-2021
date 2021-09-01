# from app.schemas.crud_postgres import (
#     ResourceCreate,
#     ResourceUpdate,
# )
from pydantic import BaseModel

from app.db.postgres.models import (
    School
)
from .crud_base import CRUDBase
from .crud_course import course
# Import CRUD object in file if need to customize crud_base
# from .crud_sample import sample
from .crud_job import job

# Or inherit CRUDBase here
school = CRUDBase[School, BaseModel, BaseModel](School)
