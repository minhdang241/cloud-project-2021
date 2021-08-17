from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import desc
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

    def get(self, db: Session, paging_params: Params):
        return paginate(db.query(self.model), paging_params)

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise EntityDoesNotExist("{0} with id {1} does not exist".format(self.model.__name__, id))
        return obj

    def get_by_fields(
            self, db: Session, order_asc=True, paging_params: Params = None, **kwargs
    ) -> Optional[ModelType]:
        """
        Get one or many records by fields. Default: get one
        order_asc:  order of id. Default: True
                    Eg: order_asc = True, get oldest record
                        order_asc = False, get latest record
        paging_params: set paging params if want to get many record
        kwargs: table fields

        Example usage:
        student.get_by_fields(db, paging_params=paging_params, grade=8)
        => Get list of students whose grade is 8
        """
        query = db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        if not order_asc:
            query = query.order_by(desc(self.model.id))
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
