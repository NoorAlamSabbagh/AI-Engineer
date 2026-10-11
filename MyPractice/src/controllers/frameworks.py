# ==============================================================================
# Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework
# File: src/controllers/frameworks.py
# Description: Controller handlers for Lec 42: Day 1
# ==============================================================================

from fastapi import HTTPException
from src.schemas.frameworks import (
    LiteLLMRequest,
    LangChainChainRequest,
    FrameworkCompareRequest,
    FrameworkCompareResponse
)
from src.services.framework_comparison import (
    execute_litellm_query,
    execute_langchain_chain,
    compare_frameworks
)


# ==============================================================================
# [Lec 42: Day 1] Handler 1: LiteLLM Unified Completion
# ==============================================================================
def handle_litellm_query(req: LiteLLMRequest):
    """[Lec 42: Day 1] Controller handler for LiteLLM unified model queries."""
    result = execute_litellm_query(
        model=req.model,
        prompt=req.prompt,
        temperature=req.temperature
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


# ==============================================================================
# [Lec 42: Day 1] Handler 2: LangChain LCEL Pipelines
# ==============================================================================
def handle_langchain_chain(req: LangChainChainRequest):
    """[Lec 42: Day 1] Controller handler for LangChain LCEL pipelines."""
    result = execute_langchain_chain(
        topic=req.topic,
        target_audience=req.target_audience,
        chain_type=req.chain_type
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


# ==============================================================================
# [Lec 42: Day 1] Handler 3: Side-by-Side Comparison
# ==============================================================================
def handle_framework_compare(req: FrameworkCompareRequest):
    """[Lec 42: Day 1] Controller handler for LiteLLM vs LangChain comparison."""
    result = compare_frameworks(
        prompt=req.prompt,
        model_name=req.model
    )
    return result
