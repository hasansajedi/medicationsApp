import pytest
from fastapi.testclient import TestClient
from starlette import status


@pytest.mark.asyncio
async def test_get_drugs_list(api_client: TestClient, default_access_token: str):
    response = api_client.get(
        "/api/drugs/",
        headers={
            "Authorization": default_access_token,
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("page, page_size, pages", [(1, 2, 100), (2, 20, 10)])
async def test_get_drugs_list_paginated(
    api_client: TestClient,
    default_access_token: str,
    page,
    page_size,
    pages,
):
    response = api_client.get(
        f"/api/drugs/?page={page}&size={page_size}",
        headers={
            "Authorization": default_access_token,
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    assert response.json()["total"] == 200
    assert response.json()["page"] == page
    assert response.json()["pages"] == pages
    assert len(response.json()["items"]) == page_size


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_keyword, total, pages_count, items_count",
    [
        ("Folic", 1, 1, 1),
        ("Disease", 99, 1, 10),
        ("aa", 1, 1, 1),
        ("invalidSearchValue", 0, 1, 0),
    ],
)
async def test_can_search_in_drugs_list(
    api_client: TestClient,
    default_access_token: str,
    search_keyword,
    total,
    pages_count,
    items_count,
):
    response = api_client.get(
        f"/api/drugs/?search={search_keyword}",
        headers={
            "Authorization": default_access_token,
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    assert response.json()["total"] == total
    assert response.json()["page"] == pages_count
    assert len(response.json()["items"]) == items_count


@pytest.mark.asyncio
async def test_cannot_get_drugs_list_without_authorization(api_client: TestClient):
    response = api_client.get("/api/drugs/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_cannot_get_drugs_list_with_invalid_access_token(api_client: TestClient):
    response = api_client.get(
        "/api/drugs/",
        headers={
            "Authorization": "Bearer invalid_access_token",
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_cannot_get_drugs_list_from_wrong_path(
    api_client_with_wrong_dataset_path: TestClient,
    default_access_token_with_wrong_dataset_path: str,
):
    response = api_client_with_wrong_dataset_path.get(
        "/api/drugs/",
        headers={
            "Authorization": default_access_token_with_wrong_dataset_path,
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "Error occurred on loading dataset."
