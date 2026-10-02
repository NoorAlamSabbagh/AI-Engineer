from fastapi import APIRouter
from src.schemas.website import WebsiteSummarizeRequest, BrochureRequest
from src.controllers.website import (
    summarize_website_controller,
    create_brochure_controller
)

router = APIRouter(
    prefix="/website",
    tags=["Website Analysis"]
)

@router.post("/summarize")
def summarize_website(request: WebsiteSummarizeRequest):
    return summarize_website_controller(request)

# New: Full Multi-page Brochure Endpoint
@router.post("/brochure")
def create_brochure(request: BrochureRequest):
    return create_brochure_controller(request)
