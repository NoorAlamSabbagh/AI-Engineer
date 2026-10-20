# ==============================================================================
# Lec 44–48: Day 2 — Gradio Web User Interfaces & Frontends
# File: src/routes/gradio_ui.py
# Description: FastAPI routes for Day 2 Swagger documentation and REST endpoints
# ==============================================================================

from fastapi import APIRouter
from src.schemas.gradio_ui import (
    TextTransformRequest,
    TextTransformResponse,
    BrochureGenerateRequest,
    BrochureGenerateResponse,
    GradioStatusResponse
)
from src.controllers.gradio_ui import (
    handle_gradio_status,
    handle_text_transform,
    handle_brochure_generate
)

router = APIRouter(
    prefix="/ui",
    tags=["Lec 44–48: Day 2 — Gradio & Interactive UIs"]
)


# ==============================================================================
# Endpoint 1: Gradio Status & Mounted App Discovery
# ==============================================================================
@router.get(
    "/info",
    summary="[Lec 44–48: Day 2] Get mounted Gradio UI status and features",
    response_model=GradioStatusResponse
)
def get_gradio_info():
    """
    Returns information about the integrated Gradio user interface:
    - **Mounted Path**: `/gradio` on the FastAPI server (e.g. `http://127.0.0.1:8000/gradio`)
    - **Lecture Range**: Lectures 44 to 48 (Gradio Day)
    - **Available Tabs**: Text Transforms, Token Streaming, and Brochure Generator
    """
    return handle_gradio_status()


# ==============================================================================
# Endpoint 2: Text Transformation (Lec 44 & 45)
# ==============================================================================
@router.post(
    "/transform",
    summary="[Lec 44–45: Day 2] Execute text transformation algorithm",
    response_model=TextTransformResponse
)
def text_transform_endpoint(request: TextTransformRequest):
    """
    Applies the selected transformation to the input text:
    - **SHOUT (Uppercase)**: Converts all text to uppercase with megaphone emoji.
    - **whisper (lowercase)**: Converts text to quiet lowercase.
    - **Reverse Text**: Reverses the string character by character.
    - **Word & Character Count**: Calculates words, characters, and vowel counts.
    """
    return handle_text_transform(request)


# ==============================================================================
# Endpoint 3: Web Scraper & Executive Brochure Generator (Lec 48 Capstone)
# ==============================================================================
@router.post(
    "/brochure",
    summary="[Lec 48: Day 2] Live web scrape and executive brochure generation",
    response_model=BrochureGenerateResponse
)
def brochure_endpoint(request: BrochureGenerateRequest):
    """
    Scrapes any live company landing page using BeautifulSoup, extracts clean text,
    and instructs OpenAI (gpt-4o-mini) to generate a structured executive brochure
    covering value propositions, key products, target audience, and talent pitch.
    """
    return handle_brochure_generate(request)
