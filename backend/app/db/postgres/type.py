from sqlalchemy.dialects.postgresql import ENUM

from app.resources.strings import CourseLevelType, CareerType

course_level_type = ENUM(CourseLevelType.BASIC, CourseLevelType.ADVANCED, name="CourseLevelType")
career_type = ENUM(
    CareerType.FE,
    CareerType.BE,
    CareerType.FULL,
    CareerType.IOS,
    CareerType.ANDROID,
    CareerType.CYBER,
    CareerType.TESTER,
    CareerType.ML,
    CareerType.DEVOPS,
    CareerType.WEB,
    CareerType.DATA,
    CareerType.SOFTWARE,
    name="CareerType"
)
