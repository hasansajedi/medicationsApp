from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.auth.schema import Token
from src.api.auth.utils import create_access_token
from src.api.dependencies.throttle import rate_limit, ThrottleTypeEnum

auth_router = APIRouter(
    tags=["auth"],
    redirect_slashes=False,
)


@auth_router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
@rate_limit(ThrottleTypeEnum.AUTH)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(
        data={"sub": form_data.username, "grant_type": form_data.grant_type},
        shared_access_key=form_data.client_secret,
    )
    return Token(access_token=access_token, token_type="bearer")
