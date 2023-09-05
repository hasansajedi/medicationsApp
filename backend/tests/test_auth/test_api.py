import pytest
from fastapi.testclient import TestClient
from starlette import status


@pytest.mark.asyncio
async def test_get_access_token(api_client: TestClient):
    data = {
        "grant_type": "password",
        "username": "username",
        "password": "password",
        "client_secret": "test",
    }

    response = api_client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    assert "access_token" in json_response


@pytest.mark.asyncio
async def test_cannot_get_access_token_without_credentials(api_client: TestClient):
    response = api_client.post("/api/auth/token")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_cannot_get_access_token_with_wrong_access_key(api_client: TestClient):
    data = {
        "grant_type": "password",
        "username": "username",
        "password": "password",
        "client_secret": "wrong_access_key",
    }

    response = api_client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
