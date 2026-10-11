# ==============================================================================
# Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework
# File: src/routes/frameworks.py
# Description: FastAPI routes for Lec 42: Day 1 endpoints
# ==============================================================================

from fastapi import APIRouter
from src.schemas.frameworks import (
    LiteLLMRequest,
    LangChainChainRequest,
    FrameworkCompareRequest,
    FrameworkCompareResponse
)
from src.controllers.frameworks import (
    handle_litellm_query,
    handle_langchain_chain,
    handle_framework_compare
)

router = APIRouter(
    prefix="/frameworks",
    tags=["Lec 42: Day 1 — LangChain vs LiteLLM"]
)


# ==============================================================================
# [Lec 42: Day 1] Endpoint 1: LiteLLM Unified Model Gateway
# ==============================================================================
@router.post(
    "/litellm",
    summary="[Lec 42: Day 1] Execute query via LiteLLM unified gateway"
)
def litellm_endpoint(request: LiteLLMRequest):
    """
    [Lec 42: Day 1] Calls any LLM provider (OpenAI, Groq, Ollama, Anthropic)
    via LiteLLM's single completion() API.
    Returns response text, execution latency, token counts, and estimated cost in USD.
    """
    return handle_litellm_query(request)


# ==============================================================================
# [Lec 42: Day 1] Endpoint 2: LangChain LCEL Declarative Pipeline
# ==============================================================================
@router.post(
    "/langchain",
    summary="[Lec 42: Day 1] Execute prompt chain via LangChain LCEL"
)
def langchain_endpoint(request: LangChainChainRequest):
    """
    [Lec 42: Day 1] Executes a composable LangChain Expression Language (LCEL) chain.
    Supports single-step prompt template pipelines or two-step sequential reasoning workflows.
    """
    return handle_langchain_chain(request)


# ==============================================================================
# [Lec 42: Day 1] Endpoint 3: LangChain vs LiteLLM Head-to-Head Comparison
# ==============================================================================
@router.post(
    "/compare",
    summary="[Lec 42: Day 1] Head-to-head comparison: LangChain vs LiteLLM",
    response_model=FrameworkCompareResponse
)
def compare_endpoint(request: FrameworkCompareRequest):
    """
    [Lec 42: Day 1] Runs the exact same prompt through both LiteLLM and LangChain concurrently.
    Returns comparative latencies, token consumption, code paradigms, and strategic guidance.
    """
    return handle_framework_compare(request)
