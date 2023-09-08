from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from starlette import status

from src.api.dependencies.throttle import rate_limit, ThrottleTypeEnum
from src.api.dependencies.token import verify_token
from src.api.drugs.schemas.medication import DrugModel
from src.api.drugs.selectors import LoadDrugDataHelper

drugs_router = APIRouter(
    tags=["drugs"],
    redirect_slashes=False,
)


@drugs_router.get(
    "/",
    description="Get list of possible drugs.",
    response_model=Page[DrugModel],
    status_code=status.HTTP_200_OK,
)
@rate_limit(ThrottleTypeEnum.PUBLIC)
async def get_drugs(
    drugs: Page[DrugModel] = Depends(LoadDrugDataHelper.load_data_from_json_file),
    token: Optional[dict] = Depends(verify_token),
):
    return drugs
