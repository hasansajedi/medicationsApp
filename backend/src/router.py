from fastapi import APIRouter

from src.api.drugs.api import drugs_router
from src.api.auth.api import auth_router

router = APIRouter()


router.include_router(drugs_router, prefix="/drugs")
router.include_router(auth_router, prefix="/auth")
