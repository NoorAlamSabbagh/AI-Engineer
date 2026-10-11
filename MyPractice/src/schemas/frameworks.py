# ==============================================================================
# Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework
# File: src/schemas/frameworks.py
# Description: Pydantic request/response schemas for Lec 42: Day 1
# ==============================================================================

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ------------------------------------------------------------------------------
# [Lec 42: Day 1] LiteLLM Request Schema
# ------------------------------------------------------------------------------
class LiteLLMRequest(BaseModel):
    """[Lec 42: Day 1] Request schema for LiteLLM unified completion calls."""
    prompt: str = Field(..., description="The user prompt to submit")
    model: str = Field("gpt-4o-mini", description="Model name in provider/model format (e.g. 'gpt-4o-mini', 'groq/llama-3.3-70b-versatile', 'ollama/llama3.2')")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")


# ------------------------------------------------------------------------------
# [Lec 42: Day 1] LangChain LCEL Request Schema
# ------------------------------------------------------------------------------
class LangChainChainRequest(BaseModel):
    """[Lec 42: Day 1] Request schema for LangChain Expression Language (LCEL) pipelines."""
    topic: str = Field(..., description="Topic or prompt for the multi-step LCEL chain")
    target_audience: str = Field("Senior Software Engineers", description="Audience persona for tone styling")
    chain_type: str = Field("two_step", description="'single_step' or 'two_step' (Analysis -> Executive Action Plan)")


# ------------------------------------------------------------------------------
# [Lec 42: Day 1] Side-by-Side Comparison Request Schema
# ------------------------------------------------------------------------------
class FrameworkCompareRequest(BaseModel):
    """[Lec 42: Day 1] Request schema to compare LiteLLM vs LangChain on the same prompt."""
    prompt: str = Field(..., description="Standard prompt to benchmark across both frameworks")
    model: str = Field("gpt-4o-mini", description="Target model to test with both frameworks")


# ------------------------------------------------------------------------------
# [Lec 42: Day 1] Framework Performance Metric Schema
# ------------------------------------------------------------------------------
class FrameworkMetric(BaseModel):
    """[Lec 42: Day 1] Standardized latency, token, and cost metric record."""
    framework: str
    response: str
    latency_seconds: float
    tokens: Optional[Dict[str, int]] = None
    cost_usd: Optional[float] = None
    code_paradigm: str


# ------------------------------------------------------------------------------
# [Lec 42: Day 1] Side-by-Side Comparison Response Schema
# ------------------------------------------------------------------------------
class FrameworkCompareResponse(BaseModel):
    """[Lec 42: Day 1] Comprehensive response returning comparative metrics and strategic advice."""
    status: str
    lecture: str = "Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework"
    prompt: str
    litellm_result: FrameworkMetric
    langchain_result: FrameworkMetric
    recommendation: Dict[str, Any]
