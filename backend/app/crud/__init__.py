from app.db.postgres.models import (
    Course,
    School,
    Job
)
# from app.schemas.crud_postgres import (
#     ResourceCreate,
#     ResourceUpdate,
# )
from pydantic import BaseModel

from .crud_base import CRUDBase

# Import CRUD object in file if need to customize crud_base
# from .crud_sample import sample

# Or inherit CRUDBase here
course = CRUDBase[Course, BaseModel, BaseModel](Course)
job = CRUDBase[Job, BaseModel, BaseModel](Job)
school = CRUDBase[School, BaseModel, BaseModel](School)
