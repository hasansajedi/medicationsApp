import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.api.dependencies.configuration import app_settings
from src.router import router

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=app_settings.title,
    version=app_settings.version,
    description=app_settings.description,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    end_time = datetime.utcnow()

    log_message = {
        "timestamp": start_time.isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "processing_time": (end_time - start_time).total_seconds(),
    }

    logger.info(log_message)

    return response


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


@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost", encoding="utf8")
    await FastAPILimiter.init(redis_client)


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()
