"""
File contains constant string or class
"""


class CourseLevelType:
    BASIC = "BASIC"
    ADVANCED = "ADVANCED"


class CareerType(object):
    FE = "Frontend Engineer"
    BE = "Backend Engineer"
    FULL = "Full-stack Engineer"
    IOS = "IOS Developer"
    ANDROID = "Android Developer"
    CYBER = "Cyber Security"
    TESTER = "Software Tester"
    ML = "ML/AI Engineer"
    DEVOPS = "DevOps"
    WEB = "Web Developer"
    DATA = "Data Engineer"
    SOFTWARE = "Software Engineer"


DEFAULT_NAMESPACE = "default"

# Error messages
EXPIRED_TOKEN = "Access Token Expired"
INVALID_TOKEN = "Invalid Token"
ERROR_TOKEN = "Verify Token Error"
INVALID_PERMISSION = "Operation is not permitted"
