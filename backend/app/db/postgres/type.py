from sqlalchemy.dialects.postgresql import ENUM

from app.resources.strings import SampleType

type_enum = ENUM(SampleType.CRAWL, SampleType.TRANSFORM, name="SampleType")
