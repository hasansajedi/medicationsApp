from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.api.dependencies.configuration import app_settings
from src.router import router

app = FastAPI(
    title=app_settings.title,
    version=app_settings.version,
    description=app_settings.description,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
)

# Allow requests from React app's domain
origins = [
    "http://0.0.0.0:3000",
    "https://0.0.0.0:3000",
    "http://0.0.0.0:8006",
    "https://0.0.0.0:8006",
    "http://localhost:3000",
    "http://localhost:8006",
    "http://127.0.0.1:8006",
    "http://172.23.0.3:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# prevent FastAPI from redirecting missing slashes to an HTTP version
app.router.redirect_slashes = False

# Import the routes from APIs
app.include_router(router, prefix=app_settings.api_prefix)


# Function to generate OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title, version=app.version, routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(content=custom_openapi())
