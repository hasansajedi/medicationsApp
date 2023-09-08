import os
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from src.api.dependencies.configuration import app_settings


@pytest.fixture
def default_app() -> FastAPI:
    set_envs()
    os.environ["DATA_PATH"] = "data/dataset.json"
    app_settings.DATA_PATH = os.environ.get("DATA_PATH", app_settings.DATA_PATH)

    from src.main import app as main_app

    yield main_app


@pytest.fixture
def default_app_with_wrong_dataset_path() -> FastAPI:
    set_envs()
    os.environ["DATA_PATH"] = "invalid_dataset.json"
    app_settings.DATA_PATH = os.environ.get("DATA_PATH", app_settings.DATA_PATH)

    from src.main import app as main_app

    yield main_app


@pytest.fixture
def api_client(default_app: FastAPI) -> TestClient:
    return TestClient(default_app)


@pytest.fixture
def api_client_with_wrong_dataset_path(
    default_app_with_wrong_dataset_path: FastAPI,
) -> TestClient:
    return TestClient(default_app_with_wrong_dataset_path)


def set_envs():
    os.environ["TITLE"] = "Test Title"
    os.environ["DESCRIPTION"] = "Test Description"
    os.environ["DEBUG"] = "True"
    os.environ["SHRED_ACCESS_KEY"] = "test"

    app_settings.title = os.environ.get("TITLE", app_settings.title)
    app_settings.description = os.environ.get("DESCRIPTION", app_settings.description)
    app_settings.debug = bool(os.environ.get("DEBUG", app_settings.debug))
    app_settings.SHRED_ACCESS_KEY = os.environ.get(
        "SHRED_ACCESS_KEY", app_settings.SHRED_ACCESS_KEY
    )
