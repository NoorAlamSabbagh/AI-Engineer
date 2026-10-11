# ==============================================================================
# Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework
# File: MyPractice/week2/day1_langchain_vs_litellm.py
# ==============================================================================
# This script directly implements the teachings of Lecture 42 (Week 2 Day 1):
# 1. Direct OpenAI Baseline (Why raw SDKs create vendor lock-in)
# 2. LiteLLM Gateway (Unified API, zero-code model swapping, cost tracking, streaming)
# 3. LangChain LCEL (PromptTemplate | Model | OutputParser pipelines & multi-step chains)
# 4. Strategic Decision Framework (When to choose LangChain vs LiteLLM vs Hybrid)
# ==============================================================================

import os
import io
import sys
import time
from dotenv import load_dotenv

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# [Lec 42: Day 1] Verify API Keys
openai_key = os.getenv("OPENAI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print("=" * 75)
print("🎓 LEC 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework")
print("=" * 75)
print(f"• OpenAI API Key configured: {'✅ Yes' if openai_key else '❌ Missing'}")
print(f"• Groq API Key configured:   {'✅ Yes' if groq_key else '❌ Optional/Missing'}")
print("-" * 75)


# ==============================================================================
# [Lec 42: Day 1] Section 1: Direct Provider SDK (The Starting Point)
# ==============================================================================
# In the lecture, Ed Donner contrasts using raw provider SDKs vs frameworks.
# Direct SDK is simple, but couples your code directly to one vendor.
# ==============================================================================
def lec42_day1_demo_direct_sdk(prompt: str):
    """
    [Lec 42: Day 1] Direct OpenAI API Call
    Demonstrates baseline single-provider code and explains why vendor lock-in occurs.
    """
    print("\n" + "=" * 65)
    print("1️⃣  [Lec 42: Day 1] Baseline: Direct Provider SDK (OpenAI)")
    print("=" * 65)
    from openai import OpenAI
    client = OpenAI()

    start_time = time.time()
    # [Lec 42: Day 1] Raw OpenAI Chat Completion call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    elapsed = time.time() - start_time
    reply = response.choices[0].message.content
    print(f"Response ({elapsed:.2f}s):\n{reply.strip()}")
    print(f"Token Usage: {response.usage.total_tokens} (Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens})")
    print("\n👉 [Lec 42: Day 1 Takeaway]: If you want to switch to Claude, Gemini, or Ollama, you must rewrite imports, client initialization, and parameter formats.")


# ==============================================================================
# [Lec 42: Day 1] Section 2: LiteLLM — Universal API Gateway & Proxy
# ==============================================================================
# Lecture Teaching:
# LiteLLM treats ALL 100+ LLMs (OpenAI, Claude, Ollama, Groq, Bedrock) as if
# they were OpenAI. It normalizes inputs, outputs, errors, and cost calculation.
# ==============================================================================
def lec42_day1_demo_litellm(prompt: str):
    """
    [Lec 42: Day 1] LiteLLM Universal Gateway Demo:
    - Part A: Single unified completion() call to OpenAI
    - Part B: Built-in cost calculation with completion_cost()
    - Part C: Seamless provider swap (OpenAI -> Groq / Ollama) with ZERO code change
    - Part D: Universal token streaming
    """
    print("\n" + "=" * 65)
    print("2️⃣  [Lec 42: Day 1] LiteLLM: The Universal Model Gateway")
    print("=" * 65)
    import litellm
    from litellm import completion, completion_cost

    # [Lec 42: Day 1] Suppress verbose debug output
    litellm.suppress_debug_info = True

    # [Lec 42: Day 1] Part A: Standard OpenAI model call via LiteLLM
    print("\n[A] [Lec 42: Day 1] Calling OpenAI (gpt-4o-mini) via LiteLLM:")
    start_time = time.time()
    resp_openai = completion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed_openai = time.time() - start_time
    print(f"Response ({elapsed_openai:.2f}s):\n{resp_openai.choices[0].message.content.strip()}")

    # [Lec 42: Day 1] Part B: Built-in Token & Cost Tracking (Course Notebook In[58])
    print("\n--- [Lec 42: Day 1] Token & Cost Breakdown (Cell 58 snippet) ---")
    print(f"Input tokens: {resp_openai.usage.prompt_tokens}")
    print(f"Output tokens: {resp_openai.usage.completion_tokens}")
    print(f"Total tokens: {resp_openai.usage.total_tokens}")
    # LiteLLM embeds calculated cost in USD inside _hidden_params["response_cost"]
    # Multiplying by 100 converts USD to cents:
    raw_cost = getattr(resp_openai, "_hidden_params", {}).get("response_cost")
    if raw_cost is not None:
        print(f"Total cost: {resp_openai._hidden_params['response_cost']*100:.4f} cents")
    else:
        # Fallback to litellm.completion_cost() if _hidden_params is omitted
        calc_cost = completion_cost(completion_response=resp_openai)
        print(f"Total cost: {calc_cost * 100:.4f} cents (via completion_cost: ${calc_cost:.6f} USD)")

    # [Lec 42: Day 1] Part C: Provider Swap with ZERO code modification
    if groq_key:
        print("\n[B] [Lec 42: Day 1] Seamlessly Swapping Provider to Groq (groq/llama-3.3-70b-versatile):")
        try:
            start_time = time.time()
            resp_groq = completion(
                model="groq/llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            elapsed_groq = time.time() - start_time
            print(f"Response ({elapsed_groq:.2f}s):\n{resp_groq.choices[0].message.content.strip()[:250]}...")
        except Exception as e:
            print(f"Groq note: {e}")
    else:
        print("\n[B] [Lec 42: Day 1] Provider Swap: Easily swap to 'anthropic/claude-3-haiku' or 'ollama/llama3.2' using the exact same completion() call!")

    # [Lec 42: Day 1] Part D: Real-Time Token Streaming
    print("\n[C] [Lec 42: Day 1] Universal Real-Time Streaming with LiteLLM:")
    print("Streaming tokens: ", end="", flush=True)
    stream_resp = completion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Write a 2-line rhyme about clean code."}],
        stream=True
    )
    for chunk in stream_resp:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
    print("\n")


# ==============================================================================
# [Lec 42: Day 1] Section 3: LangChain — LCEL & Workflow Orchestration
# ==============================================================================
# Lecture Teaching:
# LangChain is NOT an API gateway. It is an orchestration framework.
# It shines when you need to chain prompts together, build RAG pipelines, or
# create autonomous agents with tools.
# ==============================================================================
def lec42_day1_demo_langchain(topic: str):
    """
    [Lec 42: Day 1] LangChain Expression Language (LCEL) Demo:
    - Part A: Single-step composable pipeline (PromptTemplate | Model | OutputParser)
    - Part B: Multi-step sequential chain (Step 1: Technical Analysis -> Step 2: Action Roadmap)
    - Part C: Streaming with chain.stream()
    """
    print("\n" + "=" * 65)
    print("3️⃣  [Lec 42: Day 1] LangChain: Expression Language (LCEL) & Orchestration")
    print("=" * 65)
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_openai import ChatOpenAI

    # ==========================================================================
    # [Lec 42: Day 1] First Look: The Exact Lecture Notebook Snippet
    # ==========================================================================
    print("\n[A] [Lec 42: Day 1] Exact Lecture Snippet: First Look at LangChain:")
    tell_a_joke = [
        {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"}
    ]
    # Initialize LangChain ChatOpenAI model (from the lecture cell)
    first_llm = ChatOpenAI(model="gpt-5-mini")
    try:
        first_response = first_llm.invoke(tell_a_joke)
        print(f"Joke via LangChain (gpt-5-mini):\n{first_response.content.strip()}\n")
    except Exception:
        # Fallback to gpt-4o-mini if gpt-5-mini access is restricted
        first_llm = ChatOpenAI(model="gpt-4o-mini")
        first_response = first_llm.invoke(tell_a_joke)
        print(f"Joke via LangChain (gpt-4o-mini):\n{first_response.content.strip()}\n")

    # [Lec 42: Day 1] Initialize Model & Output Parser for LCEL Pipelines
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    parser = StrOutputParser()

    # [Lec 42: Day 1] Part B: Single-Step LCEL Pipe
    print("[B] [Lec 42: Day 1] Single-Step LCEL Pipeline: PromptTemplate | Model | Parser")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a pragmatic software architect explaining concepts for senior developers."),
        ("user", "Explain the concept of: {topic} in 2 concise sentences.")
    ])
    # [Lec 42: Day 1] Declarative composition using Unix pipe (|)
    chain = prompt | model | parser

    start_time = time.time()
    result = chain.invoke({"topic": topic})
    elapsed = time.time() - start_time
    print(f"Chain Result ({elapsed:.2f}s):\n{result.strip()}")

    # [Lec 42: Day 1] Part B: Multi-Step Sequential Chain
    print("\n[B] [Lec 42: Day 1] Multi-Step Sequential Chain (Decomposition -> Action Roadmap):")
    # Step 1: Technical Analysis
    step1_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an engineering lead evaluating tech stack options."),
        ("user", "What are the primary challenges when scaling: {topic}? (2 bullets)")
    ])
    chain1 = step1_prompt | model | parser

    # Step 2: Executive Roadmap Synthesis
    step2_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a VP of Engineering writing concise architectural directives."),
        ("user", "Given these scaling challenges:\n{challenges}\n\nDraft a 2-step mitigation strategy.")
    ])
    chain2 = step2_prompt | model | parser

    start_time = time.time()
    challenges = chain1.invoke({"topic": topic})
    print(f"Step 1 (Challenges identified):\n{challenges.strip()}")

    mitigation = chain2.invoke({"challenges": challenges})
    elapsed = time.time() - start_time
    print(f"\nStep 2 (Mitigation Plan synthesized in {elapsed:.2f}s):\n{mitigation.strip()}")

    # [Lec 42: Day 1] Part C: Token Streaming with LangChain
    print("\n[C] [Lec 42: Day 1] Real-Time Streaming via LangChain LCEL chain.stream():")
    print("Streaming tokens: ", end="", flush=True)
    stream_chain = (
        ChatPromptTemplate.from_template("Give one motivational sentence for programmers.")
        | model
        | parser
    )
    for token in stream_chain.stream({}):
        print(token, end="", flush=True)
    print("\n")


# ==============================================================================
# [Lec 42: Day 1] Section 4: The Framework Decision Matrix
# ==============================================================================
# Lecture Teaching:
# Summarizes Ed Donner's criteria for choosing the right tool for the job.
# ==============================================================================
def lec42_day1_print_decision_matrix():
    """
    [Lec 42: Day 1] Outputs the architectural decision matrix and recommendations.
    """
    print("\n" + "=" * 75)
    print("⚖️  [Lec 42: Day 1] THE STRATEGIC DECISION MATRIX: LANGCHAIN vs LITELLM")
    print("=" * 75)
    matrix = """
| Feature / Dimension     | LiteLLM                                 | LangChain                               |
| :---------------------- | :-------------------------------------- | :-------------------------------------- |
| **Core Nature**         | Universal Model Gateway / I/O Proxy     | Comprehensive Orchestration Framework   |
| **Mental Model**        | "One standard function for all LLMs"   | "Pipes and chains connecting components"|
| **Key Syntax**          | `completion(model=..., messages=...)`   | `prompt | model | output_parser`        |
| **Model Switching**     | Instant (change model string)           | Requires provider package / wrappers    |
| **Cost & Token Tracking**| Built-in (`completion_cost`)           | Requires LangSmith or custom callbacks  |
| **Load Balancing / Proxy| Native LiteLLM Proxy with fallbacks     | Not designed as an API proxy            |
| **Chains & Pipelines**  | Manual Python code                      | First-class declarative LCEL pipelines  |
| **RAG & Vector Stores** | None (bring your own Chroma/Qdrant)     | 100+ native VectorStore/Loader integrations|
| **Agent Tool Calling**  | Native OpenAI tool syntax               | Pre-built AgentExecutor & Tool kits     |
| **Learning Curve**      | 15 minutes                              | Moderate to Steep                       |
| **Dependency Weight**   | Lightweight (~40MB)                     | Heavy (extensive dependencies)          |

🎯 [Lec 42: Day 1 Recommendation] WHEN TO CHOOSE LITELLM:
   1. You want clean, direct LLM calls without framework bloat.
   2. You need to call multiple providers (OpenAI, Claude, Ollama, Groq) with zero code changes.
   3. You need production resilience: fallbacks, retries, rate-limiting, and cost tracking.

🎯 [Lec 42: Day 1 Recommendation] WHEN TO CHOOSE LANGCHAIN:
   1. You are building complex multi-step pipelines (RAG, multi-turn QA over documents).
   2. You are orchestrating autonomous agents that need to use external tools, APIs, and calculators.
   3. You want standardized abstractions for memory, document loaders, and embedding stores.

💡 [Lec 42: Day 1 Industry Hybrid Pattern]:
   Use LangChain for your high-level application orchestration (RAG and Chains),
   and use LiteLLM as the underlying provider gateway to access all your models!
"""
    print(matrix)
    print("=" * 75)


# ==============================================================================
# [Lec 42: Day 1] Main Execution Entrypoint
# ==============================================================================
if __name__ == "__main__":
    test_prompt = "What are the trade-offs of microservices vs monoliths in high-growth startups?"
    
    # 1. [Lec 42: Day 1] Run Direct OpenAI Baseline
    lec42_day1_demo_direct_sdk(test_prompt)

    # 2. [Lec 42: Day 1] Run LiteLLM Gateway Demo
    lec42_day1_demo_litellm(test_prompt)

    # 3. [Lec 42: Day 1] Run LangChain LCEL Demo
    lec42_day1_demo_langchain("Microservice Architecture Migration")

    # 4. [Lec 42: Day 1] Run LiteLLM Pro-Feature: Prompt Caching (Hamlet Demo)
    try:
        from demo_prompt_caching import lec42_day1_prompt_caching_demo
        lec42_day1_prompt_caching_demo()
    except Exception as e:
        print(f"\n[Note on Prompt Caching]: Run 'python week2/demo_prompt_caching.py' for dedicated test ({e})")

    # 5. [Lec 42: Day 1] Print Decision Matrix
    lec42_day1_print_decision_matrix()

