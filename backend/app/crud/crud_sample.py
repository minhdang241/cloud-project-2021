from app.db.postgres import models
from app.schemas.crud_postgres import SampleCreate, SampleUpdate
from .crud_base import CRUDBase


class CRUDSample(CRUDBase[models.Sample, SampleCreate, SampleUpdate]):
    pass


sample = CRUDSample(models.Sample)
