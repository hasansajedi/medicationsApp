import pytest

from src.api.auth.utils import create_access_token


@pytest.fixture
def default_access_token(default_app) -> str:
    access_token: str = create_access_token(
        data={"sub": "test"}, shared_access_key="test"
    )
    return f"Bearer {access_token}"


@pytest.fixture
def default_access_token_with_wrong_dataset_path(
    default_app_with_wrong_dataset_path,
) -> str:
    access_token: str = create_access_token(
        data={"sub": "test"}, shared_access_key="test"
    )
    return f"Bearer {access_token}"
