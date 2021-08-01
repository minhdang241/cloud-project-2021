from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class PostgresBase(object):
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return cls.__name__ + "s"

    @declared_attr
    def id(cls):  # pylint: disable=no-self-argument
        return Column(cls.__name__.lower() + "_id", Integer, primary_key=True)
