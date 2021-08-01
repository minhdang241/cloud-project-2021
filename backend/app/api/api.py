from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from kubernetes import config

from app.db.postgres import models
from app.db.postgres.setup_postgres import engine
from .endpoints import sample
from .securities.role_checker import user_role_checker

# For production use you are advised to use the source distribution.
config.load_kube_config()

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
auth = HTTPBearer()

router.include_router(sample.router, tags=["sample"], dependencies=[Depends(user_role_checker)])
