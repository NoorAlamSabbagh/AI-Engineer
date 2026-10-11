# 🎓 Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework

Comprehensive guide, architectural comparison, and hands-on testing guide for **Lecture 42 (Week 2 Day 1)**.

---

## 🧭 Executive Summary: Orchestration vs Abstraction

When building production LLM applications, developers encounter a crucial architectural choice:

```
                           ┌────────────────────────────────────────────────────────┐
                           │               Your Application Logic                   │
                           └──────────────────┬──────────────────┬──────────────────┘
                                              │                  │
                     ┌────────────────────────┴──────┐    ┌──────┴────────────────────────┐
                     ▼                               ▼    ▼                               ▼
       ┌───────────────────────────┐                        ┌───────────────────────────┐
       │         LangChain         │                        │          LiteLLM          │
       ├───────────────────────────┤                        ├───────────────────────────┤
       │ • Orchestration Framework │                        │ • Universal API Gateway   │
       │ • LCEL Pipelines (| pipe) │                        │ • OpenAI format for 100+  │
       │ • Chains, Memory & RAG    │                        │ • Built-in Cost & Tokens  │
       │ • Autonomous Agents       │                        │ • Proxy & Fallback Router │
       └─────────────┬─────────────┘                        └─────────────┬─────────────┘
                     │                                                    │
                     └────────────────────────┬───────────────────────────┘
                                              ▼
                             ┌─────────────────────────────────┐
                             │ LLM Providers (OpenAI, Claude,  │
                             │ Ollama, Groq, DeepSeek, etc.)   │
                             └─────────────────────────────────┘
```

| Dimension | LiteLLM | LangChain |
| :--- | :--- | :--- |
| **Primary Role** | **Unified API Gateway & Proxy** | **Application Orchestrator & Agent Framework** |
| **Core Abstraction** | `completion(model=..., messages=...)` | `chain = prompt \| model \| parser` (LCEL) |
| **Mental Model** | *"Call any LLM using the familiar OpenAI syntax"* | *"Pipe Lego blocks together into complex thinking workflows"* |
| **Primary Strength** | Eliminates multi-SDK lock-in, tracks spend & latency | Deep ecosystem for RAG, vector retrieval, and autonomous agents |
| **Footprint** | Lightweight (~40MB), zero pipeline overhead | Comprehensive, feature-rich library ecosystem |

---

## 🔍 In-Depth Framework Breakdown

### 1. LiteLLM: The Universal Model Gateway

#### What Problem It Solves
Different LLM providers (OpenAI, Anthropic, Google Gemini, Ollama, Groq, Mistral, AWS Bedrock) have different SDKs, parameter names, and response shapes:
- OpenAI uses `client.chat.completions.create(model="...", messages=[...])`
- Anthropic uses `client.messages.create(model="...", messages=[...], max_tokens=...)`
- Google uses `genai.GenerativeModel("...").generate_content(...)`

If you write code directly against each SDK, changing providers requires refactoring hundreds of lines.

#### How LiteLLM Works
LiteLLM standardizes **everything** to the OpenAI Chat Completions standard:
```python
from litellm import completion, completion_cost

# Call OpenAI
res1 = completion(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}])

# Call Claude via Anthropic (Exact same syntax!)
res2 = completion(model="claude-3-haiku-20240307", messages=[{"role": "user", "content": "Hello"}])

# Call Local Ollama (Exact same syntax!)
res3 = completion(model="ollama/llama3.2", messages=[{"role": "user", "content": "Hello"}])

# Built-in Cost Calculation:
cost = completion_cost(completion_response=res1)
print(f"Cost: ${cost:.6f} USD")
```

---

### 2. LangChain: The Orchestration Engine

#### What Problem It Solves
Real-world AI systems rarely involve just a single LLM call. They require:
1. Dynamic templating with system and few-shot prompts.
2. Multi-step reasoning (Step 1 decomposes a problem $\to$ Step 2 plans $\to$ Step 3 executes).
3. Retrieval-Augmented Generation (RAG) connecting PDFs, markdown, vector stores (Chroma, FAISS).
4. Autonomous agent loops with tool usage (web search, calculator, SQL databases).

#### How LangChain Works (LangChain Expression Language - LCEL)
LCEL uses the standard Unix pipe operator (`|`) to create composable, readable pipelines:
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an executive technology consultant for {audience}."),
    ("user", "Explain: {topic}")
])

# 2. Define Model and Output Parser
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 3. Compose LCEL Pipeline
chain = prompt | model | parser

# 4. Invoke or Stream
result = chain.invoke({"audience": "CTOs", "topic": "Event-Driven Microservices"})
```

---

## ⚖️ Strategic Decision Matrix: Which Should You Choose?

```
                                ┌───────────────────────────┐
                                │ What is your primary need?│
                                └─────────────┬─────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
     ┌──────────────────────────────────┐            ┌──────────────────────────────────┐
     │ Multi-model routing, cost        │            │ Complex multi-step reasoning,    │
     │ tracking, fallbacks, or clean    │            │ RAG with vector stores, tool-    │
     │ unified API without bloat?       │            │ calling agents, or memory?       │
     └────────────────┬─────────────────┘            └────────────────┬─────────────────┘
                      ▼                                               ▼
             ✅ Choose **LiteLLM**                           ✅ Choose **LangChain**
```

### 💡 The Production Hybrid Pattern
In enterprise architectures, you **don't have to choose just one**. The premier production pattern is:
> **Use LangChain for workflow orchestration and agent tools, and point LangChain's model calls to LiteLLM (or LiteLLM Proxy) for universal multi-model routing, load balancing, and cost tracking.**

---

## 💻 Hands-On Testing Guide

### Option 1: Standalone Terminal Test Suite
Run the dedicated lecture script with live benchmarks:

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1
python week2/day1_langchain_vs_litellm.py
```

**What this script runs:**
1. Baseline Direct OpenAI API call with token metrics.
2. LiteLLM query with real-time cost calculation and token streaming.
3. Seamless provider swap (OpenAI $\to$ Groq/Ollama) with zero code change.
4. LangChain LCEL single-step pipeline.
5. LangChain multi-step sequential chain (Technical analysis $\to$ Executive roadmap).
6. LangChain token streaming via `chain.stream()`.
7. Architectural Decision Matrix summary table.

---

### Option 2: Postman & Swagger UI Endpoints

Start the FastAPI backend:
```powershell
uvicorn src.main:app --reload
```
Interactive Swagger UI: `http://127.0.0.1:8000/docs`

---

#### 🧪 Test 1: Query Any Model via LiteLLM Gateway
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/litellm`
- **Request Body**:
```json
{
  "prompt": "What are the 3 golden rules of production LLM system design?",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}
```
- **Response**:
```json
{
  "status": "success",
  "framework": "LiteLLM",
  "model_used": "gpt-4o-mini",
  "reply": "1. Implement guardrails and validation...",
  "duration_seconds": 1.42,
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 145,
    "total_tokens": 173
  },
  "cost_usd": 0.000092,
  "paradigm": "Unified I/O Wrapper & Model Gateway"
}
```

---

#### 🧪 Test 2: Orchestrated Multi-Step Pipeline via LangChain LCEL
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/langchain`
- **Request Body**:
```json
{
  "topic": "Migrating from Monolith to Event-Driven Microservices",
  "target_audience": "VP of Engineering",
  "chain_type": "two_step"
}
```
- **Response**:
```json
{
  "status": "success",
  "framework": "LangChain",
  "chain_type": "two_step_sequential",
  "audience": "VP of Engineering",
  "step1_analysis": "Decomposing the monolith introduces network latency...",
  "step2_action_plan": "1. Establish API Gateway...\n2. Implement distributed tracing...",
  "duration_seconds": 4.15,
  "pipeline": "Chain1(Analysis) -> Chain2(Executive Roadmap)",
  "paradigm": "Multi-Step LCEL Sequential Orchestration"
}
```

---

#### 🧪 Test 3: Side-by-Side Head-to-Head Benchmark
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/compare`
- **Request Body**:
```json
{
  "prompt": "Explain database indexing to a junior backend developer in 2 sentences.",
  "model": "gpt-4o-mini"
}
```
- **Response**:
```json
{
  "status": "success",
  "prompt": "Explain database indexing to a junior backend developer in 2 sentences.",
  "litellm_result": {
    "framework": "LiteLLM",
    "response": "Database indexing creates a sorted lookup structure...",
    "latency_seconds": 0.98,
    "tokens": { "total_tokens": 48 },
    "cost_usd": 0.000028,
    "code_paradigm": "Standard completion(model=..., messages=...) call"
  },
  "langchain_result": {
    "framework": "LangChain",
    "response": "An index acts like the index at the back of a textbook...",
    "latency_seconds": 1.12,
    "code_paradigm": "LCEL Pipeline: (prompt | model | parser).invoke()"
  },
  "recommendation": {
    "choose_litellm_when": [
      "You want multi-provider interoperability (swap OpenAI, Claude, Ollama, Groq seamlessly)",
      "You need production gateway features: fallbacks, retries, cost tracking, token budgeting"
    ],
    "choose_langchain_when": [
      "You are constructing complex multi-step pipelines or agentic workflows with tools and memory",
      "You need built-in connectors for vector stores (RAG) and document loaders"
    ],
    "hybrid_pattern": "Use LangChain for high-level workflow orchestration, and route model calls through LiteLLM for universal provider access and rate-limit/cost management."
  }
}
```
