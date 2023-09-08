from typing import Optional, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.api.dependencies.configuration import app_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_shared_access_key(shared_access_key: str) -> bool:
    """
    Validate if the provided shared access key matches the configured access key.

    Args:
        shared_access_key (str): The shared access key to validate.

    Returns:
        bool: True if the shared access key is valid, False otherwise.
    """
    return app_settings.SHRED_ACCESS_KEY == shared_access_key


def verify_token(access_token: str = Depends(oauth2_scheme)) -> Optional[Dict]:
    """
    Verify and decode given access token.

    Args:
        access_token (str, optional): The access token to verify.

    Returns:
        dict: The payload of the decoded token.

    Raises:
        HTTPException: If the token is invalid or unauthorized.
    """
    try:
        payload = jwt.decode(
            access_token,
            app_settings.SHRED_ACCESS_KEY,
            algorithms=[app_settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
