import datetime
from typing import Dict, List, Union

import docker
from fastapi_pagination import Params
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.crud.crud_request import RequestCreate, RequestUpdate
from app.resources.strings import RequestStatus


def get_requests(db_session: Session, paging_params: Params, order_field: str):
    resp = crud.request.filter_by(db_session, paging_params=paging_params, order_field=order_field)
    return resp


def create_request(db_session: Session):
    obj_in = RequestCreate(
        status=RequestStatus.RUNNING,
        created_success=True
    )
   
    # start the container here to crawl data
    obj = crud.request.create(db_session, obj_in=obj_in)
    environment = {'REQUEST_ID': obj.id,
                   'LIMIT_JOB': settings.LIMIT_JOB,
                   'LIMIT_CAREERS': settings.LIMIT_CAREERS,
                   'LIMIT_PAGE': settings.LIMIT_PAGE,
                   'UPDATE_REQUEST_URL': settings.UPDATE_REQUEST_URL,
                   'AWS_ACCESS_KEY': settings.AWS_ACCESS_KEY,
                   'AWS_SECRET_KEY': settings.AWS_SECRET_KEY,
                   'AWS_REGION': settings.AWS_REGION,
                   'ACCESS_TOKEN': settings.ACCESS_TOKEN,
                   'SENDER': settings.SENDER,
                   'RECIPIENT': settings.RECIPIENT,
                   'POSTGRES_USER': settings.POSTGRES_USER,
                   'POSTGRES_PASSWORD': settings.POSTGRES_PASSWORD,
                   'POSTGRES_HOST': settings.POSTGRES_HOST,
                   'POSTGRES_PORT': settings.POSTGRES_PORT,
                   'POSTGRES_DB_NAME': settings.POSTGRES_DB_NAME}
    image = settings.CRAWLER_IMAGE
    success = run_docker_container(image, environment)
    if not success:
        data = {
            'status': RequestStatus.ERROR,
        }
        obj = update_request(db_session, data)

    return success, obj


def get_request_by_id(db_session: Session, request_id: int):
    return crud.request.get_by_id(db_session, request_id)


def update_request(db_session: Session, data: dict):
    db_obj = crud.request.get_by_id(db_session, data.get('request_id'))
    obj_in = RequestUpdate(
        status=data.get('status', ''),
        updated_at=data.get('updated_at', str(datetime.datetime.utcnow)),
        request_metadata=data.get('request_metadata')
    )
    success = True
    obj = None
    try:
        obj = crud.request.update(db_session, db_obj=db_obj, obj_in=obj_in)
    except Exception as e:
        success = False
    return success, obj


def run_docker_container(image: str, environment: Union[Dict, List], detach=True):
    client = docker.from_env()
    success = True
    try:
        client.containers.run(image, environment=environment, detach=detach)
    except Exception as e:
        success = False
    return success
