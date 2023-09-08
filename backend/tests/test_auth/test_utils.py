import pytest
from fastapi import HTTPException

from src.api.auth.utils import create_access_token, GrantTypeEnum


@pytest.mark.asyncio
async def test_cannot_create_access_token_with_wrong_access_key(default_app):
    with pytest.raises(HTTPException):
        create_access_token(
            data={"sub": "test", "grant_type": GrantTypeEnum.PASSWORD.value},
            shared_access_key="wrong_access_key",
        )


@pytest.mark.asyncio
async def test_create_access_token(default_app):
    result = create_access_token(
        data={"sub": "test", "grant_type": GrantTypeEnum.PASSWORD.value},
        shared_access_key="test",
    )
    assert result
