import logging
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose.exceptions import ExpiredSignatureError, JWTError
from keycloak import KeycloakOpenID

from app.core.config import settings
from app.resources import strings

logger = logging.getLogger()

auth = HTTPBearer()


class RoleChecker:
    def __init__(self, allowed_roles: Optional[List] = None):
        self.allowed_roles = allowed_roles

    def __call__(self, authorization: HTTPAuthorizationCredentials = Depends(auth)) -> str:
        """
        Function to verify access token
        Check user role access

        Return: user id
        """
        access_token = authorization.credentials
        keycloak_config = settings.KEYCLOAK_CONFIG
        keycloak_openid = KeycloakOpenID(
            server_url=keycloak_config["server_url"],
            client_id=keycloak_config["client_id"],
            realm_name=keycloak_config["realm_name"],
            client_secret_key=keycloak_config["client_secret_key"],
        )

        # Add header for the public key to comply with the decoding policy
        certs = keycloak_openid.certs()
        options = {"verify_signature": True,
                   "verify_aud": False, "verify_exp": True}
        try:
            token_info = keycloak_openid.decode_token(
                access_token, key=certs, options=options)

        except ExpiredSignatureError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.EXPIRED_TOKEN
            ) from err

        except JWTError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.INVALID_TOKEN
            ) from err

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=strings.ERROR_TOKEN
            ) from err

        if not self.verify_role(token_info):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.INVALID_PERMISSION)

        try:
            user_id = token_info["sub"]
        except KeyError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.INVALID_TOKEN
            ) from err
        return user_id

    def verify_role(self, token_info: dict) -> bool:
        if not self.allowed_roles:
            # If allowed roles are not defined, route is public to all login user
            return True
        user_roles = token_info.get("realm_access").get("roles")
        for role in user_roles:
            if role in self.allowed_roles:
                return True
        return False


admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker()
