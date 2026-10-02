

from fastapi import APIRouter

from app.schemas.website import (
    Create_Brochure_Request
)

from app.controllers.website import(
    create_brochure
)

router=APIRouter(
    prefix="/website",
    tags=["Website"]
)

@router.post(
    "/"
)
def create_Broch(request:Create_Brochure_Request):
    return create_brochure(request)
