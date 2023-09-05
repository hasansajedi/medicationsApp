import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class AppGlobalConfigModel(BaseModel):
    title: str = Field(default=os.environ.get("TITLE"))
    version: str = "1.0.0"
    description: str = Field(default=os.environ.get("DESCRIPTION"))
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"
    debug: bool = Field(default=bool(os.environ.get("DEBUG")))
    SHRED_ACCESS_KEY: str = Field(default=str(os.environ.get("SHRED_ACCESS_KEY")))
    DATA_PATH: str = Field(default=str(os.environ.get("DATA_PATH")))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )


app_settings = AppGlobalConfigModel()
