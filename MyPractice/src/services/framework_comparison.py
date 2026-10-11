# ==============================================================================
# Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework
# File: src/services/framework_comparison.py
# Description: Service layer implementing LiteLLM and LangChain LCEL pipelines
# ==============================================================================

import time
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# [Lec 42: Day 1] Framework Imports
import litellm
from litellm import completion, completion_cost

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# ==============================================================================
# [Lec 42: Day 1] Function 1: Execute LiteLLM Unified Completion
# ==============================================================================
def execute_litellm_query(model: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
    """
    [Lec 42: Day 1] Executes a unified LLM call using LiteLLM.
    LiteLLM provides a standardized OpenAI-compatible interface across 100+ model providers.
    """
    start_time = time.time()
    try:
        # [Lec 42: Day 1] Calling LiteLLM universal completion API
        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": "You are a concise, expert AI Engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        duration = round(time.time() - start_time, 3)

        reply_text = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }

        # [Lec 42: Day 1] Calculate cost via LiteLLM's built-in cost dictionary
        try:
            cost = completion_cost(completion_response=response)
        except Exception:
            cost = 0.0

        return {
            "status": "success",
            "lecture": "Lec 42: Day 1",
            "framework": "LiteLLM",
            "model_used": model,
            "reply": reply_text,
            "duration_seconds": duration,
            "usage": usage,
            "cost_usd": round(cost, 6) if cost else None,
            "paradigm": "Unified I/O Wrapper & Model Gateway"
        }
    except Exception as e:
        return {
            "status": "error",
            "lecture": "Lec 42: Day 1",
            "framework": "LiteLLM",
            "model_used": model,
            "error": str(e),
            "duration_seconds": round(time.time() - start_time, 3)
        }


# ==============================================================================
# [Lec 42: Day 1] Function 2: Execute LangChain LCEL Declarative Pipeline
# ==============================================================================
def execute_langchain_chain(topic: str, target_audience: str = "Engineers", chain_type: str = "single_step") -> Dict[str, Any]:
    """
    [Lec 42: Day 1] Executes an orchestrated LLM pipeline using LangChain Expression Language (LCEL).
    Demonstrates PromptTemplate | Model | OutputParser pipelines and multi-step composition.
    """
    start_time = time.time()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "lecture": "Lec 42: Day 1",
            "framework": "LangChain",
            "error": "OPENAI_API_KEY is not configured in .env",
            "duration_seconds": 0.0
        }

    try:
        # [Lec 42: Day 1] Initialize Model & Output Parser
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        parser = StrOutputParser()

        if chain_type == "single_step":
            # [Lec 42: Day 1] Single-step prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert technical educator explaining concepts for {audience}."),
                ("user", "Explain this topic clearly and concisely in 3 bullet points: {topic}")
            ])
            # [Lec 42: Day 1] LCEL Pipeline composition: Prompt | Model | Parser
            chain = prompt | model | parser
            result = chain.invoke({"audience": target_audience, "topic": topic})

            duration = round(time.time() - start_time, 3)
            return {
                "status": "success",
                "lecture": "Lec 42: Day 1",
                "framework": "LangChain",
                "chain_type": "single_step",
                "audience": target_audience,
                "reply": result,
                "duration_seconds": duration,
                "pipeline": "ChatPromptTemplate | ChatOpenAI | StrOutputParser",
                "paradigm": "Declarative LCEL Orchestration Pipeline"
            }

        else:
            # [Lec 42: Day 1] Two-Step Sequential Pipeline (Analysis -> Action Plan)
            # Step 1: Core Technical Decomposition
            step1_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a systems architect specializing in high-throughput systems."),
                ("user", "Analyze the technical requirements and core trade-offs of: {topic}. Keep it to 2 concise paragraphs.")
            ])
            chain1 = step1_prompt | model | parser
            analysis = chain1.invoke({"topic": topic})

            # Step 2: Synthesize into an Executive Action Plan for the target audience
            step2_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a CTO synthesizing architecture decisions into executive action items for {audience}."),
                ("user", "Based on this technical analysis:\n{analysis}\n\nProduce an actionable 3-point implementation roadmap.")
            ])
            chain2 = step2_prompt | model | parser
            action_plan = chain2.invoke({"audience": target_audience, "analysis": analysis})

            duration = round(time.time() - start_time, 3)
            return {
                "status": "success",
                "lecture": "Lec 42: Day 1",
                "framework": "LangChain",
                "chain_type": "two_step_sequential",
                "audience": target_audience,
                "step1_analysis": analysis,
                "step2_action_plan": action_plan,
                "duration_seconds": duration,
                "pipeline": "Chain1(Analysis) -> Chain2(Executive Roadmap)",
                "paradigm": "Multi-Step LCEL Sequential Orchestration"
            }

    except Exception as e:
        return {
            "status": "error",
            "lecture": "Lec 42: Day 1",
            "framework": "LangChain",
            "error": str(e),
            "duration_seconds": round(time.time() - start_time, 3)
        }


# ==============================================================================
# [Lec 42: Day 1] Function 3: Side-by-Side Comparison & Decision Matrix
# ==============================================================================
def compare_frameworks(prompt: str, model_name: str = "gpt-4o-mini") -> Dict[str, Any]:
    """
    [Lec 42: Day 1] Runs a head-to-head comparison of LiteLLM vs LangChain on the same exact prompt.
    """
    # [Lec 42: Day 1] Run LiteLLM execution
    t0 = time.time()
    try:
        litellm_resp = completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        litellm_time = round(time.time() - t0, 3)
        litellm_content = litellm_resp.choices[0].message.content
        litellm_tokens = {
            "prompt_tokens": litellm_resp.usage.prompt_tokens,
            "completion_tokens": litellm_resp.usage.completion_tokens,
            "total_tokens": litellm_resp.usage.total_tokens
        }
        try:
            litellm_cost = completion_cost(completion_response=litellm_resp)
        except Exception:
            litellm_cost = 0.0
    except Exception as e:
        litellm_time = round(time.time() - t0, 3)
        litellm_content = f"Error: {e}"
        litellm_tokens = None
        litellm_cost = None

    # [Lec 42: Day 1] Run LangChain LCEL execution
    t1 = time.time()
    try:
        lc_model = ChatOpenAI(model=model_name, temperature=0.7)
        lc_prompt = ChatPromptTemplate.from_messages([("user", "{user_prompt}")])
        lc_parser = StrOutputParser()
        lc_chain = lc_prompt | lc_model | lc_parser
        lc_content = lc_chain.invoke({"user_prompt": prompt})
        lc_time = round(time.time() - t1, 3)
    except Exception as e:
        lc_time = round(time.time() - t1, 3)
        lc_content = f"Error: {e}"

    # [Lec 42: Day 1] Synthesize comparative metrics and recommendation
    return {
        "status": "success",
        "lecture": "Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework",
        "prompt": prompt,
        "litellm_result": {
            "framework": "LiteLLM",
            "response": litellm_content,
            "latency_seconds": litellm_time,
            "tokens": litellm_tokens,
            "cost_usd": round(litellm_cost, 6) if litellm_cost else None,
            "code_paradigm": "Standard completion(model=..., messages=...) call"
        },
        "langchain_result": {
            "framework": "LangChain",
            "response": lc_content,
            "latency_seconds": lc_time,
            "tokens": None,
            "cost_usd": None,
            "code_paradigm": "LCEL Pipeline: (prompt | model | parser).invoke()"
        },
        "recommendation": {
            "choose_litellm_when": [
                "You want multi-provider interoperability (swap OpenAI, Claude, Ollama, Groq seamlessly)",
                "You need production gateway features: fallbacks, retries, cost tracking, token budgeting",
                "You prefer writing native, readable Python without heavy framework overhead"
            ],
            "choose_langchain_when": [
                "You are constructing complex multi-step pipelines or agentic workflows with tools and memory",
                "You need built-in connectors for vector stores (RAG), document loaders, and embedding splitters",
                "You want standardized composable components using LCEL pipelines"
            ],
            "hybrid_pattern": "Use LangChain for high-level workflow orchestration, and route model calls through LiteLLM for universal provider access and rate-limit/cost management."
        }
    }
