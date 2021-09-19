from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

from app.api.dependencies import request
from app.resources.utils import get_db
from app.schemas.request import request as schema_request, response
from app.api.securities.cognito_auth import auth

router = APIRouter()


@router.get("/requests", response_model=Page[response.Request], dependencies=[Depends(auth.scope(["admin"]))])
def get_requests(
        order_field: str = None,
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db),
):
    resp = request.get_requests(db_session, paging_params, order_field)
    return resp


@router.get("/requests/{request_id}", response_model=response.Request, dependencies=[Depends(auth.scope(["admin"]))])
def get_requests(
        request_id: int,
        db_session: Session = Depends(get_db),
):
    resp = request.get_request_by_id(db_session, request_id)
    return resp


@router.post("/requests")
def create_request(
        db_session: Session = Depends(get_db),
):
    success, obj = request.create_request(db_session)
    return {"message": f"Create request {'successfully' if success else 'failed'}", "created_object": obj}


@router.put("/requests", dependencies=[Depends(auth.scope(["admin"]))])
def update_request(
        data: schema_request.Request,
        db_session: Session = Depends(get_db),
):
    data = data.__dict__
    success, obj = request.update_request(db_session, data)
    return {"message": f"Update request {'successfully' if success else 'failed'}", "updated_obj": obj}
