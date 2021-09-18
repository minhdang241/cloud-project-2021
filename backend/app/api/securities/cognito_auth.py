from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser
from app.core.config import settings
from pydantic import BaseModel

auth = Cognito(
    region=settings.AWS_REGION,
    userPoolId=settings.AWS_COGNITO_USER_POOL,
    client_id=settings.AWS_COGNITO_CLIENT_ID
)

class UserInfo(BaseModel):
    sub: str
    username: str