from fastapi import APIRouter
from src.schemas.models import ModelQueryRequest, BenchmarkRequest
from src.controllers.models import (
    get_providers_controller,
    query_model_controller,
    stream_model_controller,
    benchmark_controller
)

router = APIRouter(
    prefix="/models",
    tags=["Week 2 Day 1 - Multi-Provider & Local Models"]
)

@router.get("/providers")
def list_providers():
    """Returns availability and installed models for local Ollama, OpenAI, and Groq."""
    return get_providers_controller()

@router.post("/query")
def query_model(request: ModelQueryRequest):
    """
    Query any supported LLM provider:
    - 'ollama' (Local: llama3.2, deepseek-r1:1.5b, phi3, etc.)
    - 'openai' (Cloud: gpt-4o-mini)
    - 'groq' (Cloud: qwen/qwen3.8-27b)
    """
    return query_model_controller(request)

@router.post("/stream")
def stream_model(request: ModelQueryRequest):
    """Real-time token streaming response from any supported provider."""
    return stream_model_controller(request)

@router.post("/benchmark")
def benchmark_models_endpoint(request: BenchmarkRequest):
    """Compare latency and responses between local Ollama and cloud OpenAI for the same prompt."""
    return benchmark_controller(request)
