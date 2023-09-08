import datetime
from enum import StrEnum
from functools import wraps
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt
from src.api.dependencies.configuration import app_settings
from src.api.dependencies.token import validate_shared_access_key
from src.utils.logger import print_log


class GrantTypeEnum(StrEnum):
    PASSWORD = "password"


def validate_grant_type():
    """
    Decorator to validate the 'grant_type' inside the 'data' dictionary.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The decorated function.

    Raises:
        HTTPException: If the 'grant_type' is missing or not equal to 'GrantTypeEnum.PASSWORD.value'.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(data, shared_access_key, expires_delta=None):
            if (
                "grant_type" not in data
                or data["grant_type"] != GrantTypeEnum.PASSWORD.value
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid grant_type.",
                )
            return func(data, shared_access_key, expires_delta)

        return wrapper

    return decorator


@validate_grant_type()
def create_access_token(
    data: dict, shared_access_key: str, expires_delta: datetime.timedelta = None
) -> Optional[str]:
    """
    Create an access token using the provided data and shared access key.

    Args:
        data (dict): The data to include in the access token.
        shared_access_key (str): The shared access key to sign the token.
        expires_delta (datetime.timedelta, optional): The expiration time delta.
            If not provided, the default expiration time from app settings is used.

    Returns:
        str: The encoded access token.

    Raises:
        HTTPException: If the shared access key is invalid or missing.
    """
    if validate_shared_access_key(shared_access_key):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, app_settings.SHRED_ACCESS_KEY, algorithm=app_settings.ALGORITHM
        )
        print_log(data=f"AccessToken created for `{data['sub']}` user.")
        return encoded_jwt
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )
