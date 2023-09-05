from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.auth.schema import Token
from src.api.auth.utils import create_access_token

auth_router = APIRouter(
    tags=["auth"],
    redirect_slashes=False,
)


@auth_router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(
        data={"sub": form_data.username}, shared_access_key=form_data.client_secret
    )
    return Token(access_token=access_token, token_type="bearer")
