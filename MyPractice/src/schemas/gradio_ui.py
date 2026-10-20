# ==============================================================================
# Lec 44–48: Day 2 — Gradio Web User Interfaces & Frontends
# File: src/schemas/gradio_ui.py
# Description: Pydantic request and response schemas for Day 2 Swagger Docs
# ==============================================================================

from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class TextTransformRequest(BaseModel):
    text: str = Field(
        ...,
        description="Input text string to transform",
        examples=["Artificial Intelligence Engineering is Transforming Tech"]
    )
    mode: Literal[
        "SHOUT (Uppercase)",
        "whisper (lowercase)",
        "Reverse Text",
        "Word & Character Count"
    ] = Field(
        default="SHOUT (Uppercase)",
        description="Transformation style to apply to the input text",
        examples=["SHOUT (Uppercase)"]
    )


class TextTransformResponse(BaseModel):
    status: str = Field("success", description="Status of the operation")
    original_text: str = Field(..., description="Original input text")
    mode: str = Field(..., description="Mode applied")
    result: str = Field(..., description="Transformed text result")


class BrochureGenerateRequest(BaseModel):
    company_name: str = Field(
        ...,
        description="Name of the company",
        examples=["Hugging Face"]
    )
    url: str = Field(
        ...,
        description="URL of the company landing page",
        examples=["https://huggingface.co"]
    )
    model: Optional[str] = Field(
        default="gpt-4o-mini",
        description="LLM engine to generate brochure (gpt-4o-mini or local llama3.2)",
        examples=["gpt-4o-mini"]
    )


class BrochureGenerateResponse(BaseModel):
    status: str = Field("success", description="Status of the operation")
    company_name: str = Field(..., description="Company name")
    url: str = Field(..., description="Scraped URL")
    model_used: str = Field(..., description="Model used for generation")
    scraped_characters: int = Field(..., description="Number of characters extracted from page")
    brochure_markdown: str = Field(..., description="Complete executive marketing brochure in Markdown format")


class GradioStatusResponse(BaseModel):
    status: str = Field("active", description="Status of the Gradio integration")
    lecture_range: str = Field("Lec 44–48", description="Course lecture range for Day 2")
    mounted_path: str = Field("/gradio", description="FastAPI route where Gradio UI is mounted")
    browser_url: str = Field("http://127.0.0.1:8000/gradio", description="Full URL to access the Gradio UI in browser")
    available_tabs: List[str] = Field(
        ...,
        description="Interactive tabs available in the Gradio interface"
    )
    supported_models: List[str] = Field(
        ...,
        description="Supported AI models in the UI"
    )
