from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.db.errors import EntityDoesNotExist
from app.db.postgres.base_class import PostgresBase

ModelType = TypeVar("ModelType", bound=PostgresBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to create, read, update and delete
        """
        self.model = model

    def get(self, db: Session, paging_params: Params = None, fields: List[str] = None):
        if fields:
            query = db.query(*[getattr(self.model, key) for key in fields])
        else:
            query = db.query(self.model)
        return paginate(query, paging_params) if paging_params else query.all()

    def get_field_by_id(self, db: Session, id: Any, paging_params: Params = None, fields: List[str] = None):
        if fields:
            query = db.query(*[getattr(self.model, key) for key in fields])
        else:
            query = db.query(self.model)
        return query.filter(self.model.id == id).first()

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise EntityDoesNotExist("{0} with id {1} does not exist".format(self.model.__name__, id))
        return obj

    def filter_by(self, db: Session, order_desc=True, paging_params: Params = None, **kwargs) -> Union[Page, List]:
        query = db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                if type(value) == list:
                    query = query.filter(getattr(self.model, key).in_(value))
                else:
                    query = query.filter(getattr(self.model, key) == value)
        if order_desc:
            query = query.order_by(desc(self.model.id))
        else:
            query = query.order_by(asc(self.model.id))
        return paginate(query, paging_params) if paging_params else query.all()

    def get_by_fields(
            self, db: Session, order_asc=True, paging_params: Params = None, sorted_by: str = None, **kwargs
    ) -> Optional[ModelType]:
        query = db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        sorted_attr = getattr(self.model, sorted_by) if sorted_by else self.model.id
        if not order_asc:
            query = query.order_by(desc(sorted_attr))
        else:
            query = query.order_by(asc(sorted_attr))
        return paginate(query, paging_params) if paging_params else query.first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
