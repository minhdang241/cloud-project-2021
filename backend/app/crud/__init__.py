# from app.db.postgres.models import (
#     RequestResource,
# )
# from app.schemas.crud_postgres import (
#     ResourceCreate,
#     ResourceUpdate,
# )

from .crud_base import CRUDBase

# Import CRUD object in file if need to customize crud_base
from .crud_sample import CRUDSample

# Or inherit CRUDBase here
# resource = CRUDBase[RequestResource, ResourceCreate, ResourceUpdate](RequestResource)
