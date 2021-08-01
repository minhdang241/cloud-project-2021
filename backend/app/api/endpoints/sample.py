from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.resources.utils import get_db
from app.schemas.sample import request, response
from ..securities.role_checker import user_role_checker

router = APIRouter()
auth = HTTPBearer()


@router.post("/samples", response_model=response.SampleDTO)
def create_sample(
        data: request.SampleDTO,
        authorization: HTTPAuthorizationCredentials = Depends(auth),
        user_id: str = Depends(user_role_checker),
        db_session: Session = Depends(get_db),
) -> response.SampleDTO:
    pass
