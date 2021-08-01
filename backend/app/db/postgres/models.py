import datetime

from sqlalchemy import (Column, String, TIMESTAMP)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from .setup_postgres import Base


class Sample(Base):
    user_id = Column(String)
    request_name = Column(String)
    schedule = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.datetime.utcnow)
    request_metadata = Column(
        "metadata", mutable_json_type(dbtype=JSONB, nested=True))

    resources = relationship("RequestResource", back_populates="request")
