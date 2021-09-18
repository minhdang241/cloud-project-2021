from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.db.postgres import models
from app.db.postgres.setup_postgres import engine
from .endpoints import recommendation, request, sample

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
auth = HTTPBearer()

router.include_router(sample.router, tags=["sample"])
router.include_router(request.router, tags=["request"])
router.include_router(recommendation.router, tags=["recommendation"], prefix="/recommendation")
