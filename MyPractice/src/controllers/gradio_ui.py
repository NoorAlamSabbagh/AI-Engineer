# ==============================================================================
# Lec 44–48: Day 2 — Gradio Web User Interfaces & Frontends
# File: src/controllers/gradio_ui.py
# Description: HTTP Controllers bridging FastAPI endpoints to the Gradio service layer
# ==============================================================================

from fastapi import HTTPException
from src.schemas.gradio_ui import (
    TextTransformRequest,
    TextTransformResponse,
    BrochureGenerateRequest,
    BrochureGenerateResponse,
    GradioStatusResponse
)
from src.services.gradio_service import transform_text, generate_brochure_sync


def handle_gradio_status() -> GradioStatusResponse:
    """Returns the operational status of the mounted Gradio UI."""
    return GradioStatusResponse(
        status="active",
        lecture_range="Lec 44–48",
        mounted_path="/gradio",
        browser_url="http://127.0.0.1:8000/gradio",
        available_tabs=[
            "Tab 1: 🚀 Gradio 101 Basics (Lec 44 & 45)",
            "Tab 2: ⚡ Real-Time LLM Token Streaming (Lec 46 & 47)",
            "Tab 3: 🏢 AI Company Brochure Generator (Lec 48 Capstone)"
        ],
        supported_models=["OpenAI (gpt-4o-mini)", "Local Ollama (llama3.2)"]
    )


def handle_text_transform(request: TextTransformRequest) -> TextTransformResponse:
    """Applies the selected text transformation."""
    try:
        result = transform_text(request.text, request.mode)
        return TextTransformResponse(
            status="success",
            original_text=request.text,
            mode=request.mode,
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text transformation error: {str(e)}")


def handle_brochure_generate(request: BrochureGenerateRequest) -> BrochureGenerateResponse:
    """Scrapes target website and generates an executive Markdown brochure."""
    try:
        res = generate_brochure_sync(
            company_name=request.company_name,
            url=request.url,
            model=request.model or "gpt-4o-mini"
        )
        if res.get("error") and res["scraped_chars"] == 0:
            raise HTTPException(status_code=400, detail=res["error"])

        return BrochureGenerateResponse(
            status="success",
            company_name=request.company_name,
            url=request.url,
            model_used=request.model or "gpt-4o-mini",
            scraped_characters=res["scraped_chars"],
            brochure_markdown=res["brochure"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brochure generation error: {str(e)}")
