# 📚 AI Engineering Master Practice Guide — Week-by-Week & Day-by-Day

Comprehensive testing guide for all exercises and API endpoints built across **Week 1** and **Week 2**.

---

## ⚡ Quick Server Startup

Whenever you want to test in **Postman** or **Swagger UI**:

```powershell
# 1. Open terminal and navigate to your project
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"

# 2. Activate Python virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Start FastAPI server
uvicorn src.main:app --reload
```

- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Required Header for all POST requests**:
  ```http
  Content-Type: application/json
  ```

---

## 🏛️ WEEK 1: Foundations of LLMs & Web Intelligence

---

### Week 1 • Day 1: Connecting to Frontier Models & Simple Ask
*Demonstrates calling OpenAI's Chat Completions API with a single user prompt.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/ask`
- **Request Body**:
```json
{
  "prompt": "What is an LLM in two sentences?"
}
```
- **Expected Response**:
```json
{
  "status": "success",
  "prompt": "What is an LLM in two sentences?",
  "reply": "A Large Language Model (LLM) is an AI algorithm trained on vast amounts of text to recognize, generate, and process human language. It predicts the most likely next tokens to perform tasks such as answering questions, summarizing, and writing code."
}
```
- **Terminal Equivalent**: `python week1/day1_intro.py`

---

### Week 1 • Day 2: Prompt Engineering & System Roles
*Tests steerability using system prompts to constrain tone and format.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/ask`
- **Request Body**:
```json
{
  "prompt": "Explain quantum computing to a 7-year-old using a pirate accent."
}
```
- **Terminal Equivalent**: `python week1/day2_prompting.py`

---

### Week 1 • Day 3 & Day 4: Web Scraping & Single-Page Summarizer
*Fetches real HTML via BeautifulSoup, cleans boilerplate/scripts, and feeds sanitized text to the LLM with a customizable tone.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/website/summarize`
- **Request Body**:
```json
{
  "url": "https://example.com",
  "tone": "enthusiastic and professional"
}
```
- **Expected Response**:
```json
{
  "status": "success",
  "url": "https://example.com",
  "tone": "enthusiastic and professional",
  "summary": "Example Domain is a clean, designated website established by IANA for illustrative examples in documentation..."
}
```
- **Terminal Equivalent**: `python week1/scraper.py` & `python week1/day4_summarizer.py`

---

### Week 1 • Day 5: Multi-Page Web Brochure Generator (Capstone)
*Deep scraping that follows internal hyperlinks across the website, summarizes multiple sections, and generates a cohesive marketing brochure.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/website/brochure`
- **Request Body**:
```json
{
  "company_name": "Edward Donner",
  "url": "https://edwarddonner.com"
}
```
- **Expected Response**:
```json
{
  "status": "success",
  "company_name": "Edward Donner",
  "url": "https://edwarddonner.com",
  "brochure": "# Edward Donner — AI Engineering Education\n\n## Overview\n..."
}
```
- **Terminal Equivalent**: `python week1/day5_brochure.py`

---

### Week 1 • Bonus: Multi-Turn Conversation Memory
*Stateful chat loop where conversation history is retained and sent back for context awareness.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/conversation/`

#### Step 1: Start Conversation
- **Request Body**:
```json
{
  "message": "Hi, my name is Alam and I am building an AI Engineering backend."
}
```

#### Step 2: Follow-up message (Pass back the received `conversation_history`)
- **Request Body**:
```json
{
  "message": "What is my name and what project am I working on?",
  "history": [
    {
      "role": "user",
      "content": "Hi, my name is Alam and I am building an AI Engineering backend."
    },
    {
      "role": "assistant",
      "content": "Hello Alam! You are building an AI Engineering backend. How can I help you today?"
    }
  ]
}
```
- **Expected Response**: AI accurately recalls your name and project because history was preserved in the payload.

---

## 🚀 WEEK 2: Frontier APIs, Local Models, Reasoning & Multi-Agent Systems

---

### Week 2 • Day 1 • Test 1: Discover Providers & Local Models
*Checks Ollama status at `http://localhost:11434`, lists all installed local models, and verifies Cloud API keys (OpenAI, Groq).*

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/models/providers`
- **Request Body**: None
- **Expected Response**:
```json
{
  "status": "success",
  "providers": {
    "ollama": {
      "available": true,
      "type": "local",
      "endpoint": "http://localhost:11434/v1",
      "installed_models": ["llama3.2:latest", "deepseek-r1:1.5b", "phi3:latest", "qwen3:4b"],
      "default_model": "llama3.2"
    },
    "openai": {
      "available": true,
      "type": "cloud",
      "default_model": "gpt-4o-mini"
    },
    "groq": {
      "available": true,
      "type": "cloud",
      "default_model": "qwen/qwen3.8-27b"
    }
  }
}
```

---

### Week 2 • Day 1 • Test 2: Unified Query (Local Ollama vs Cloud OpenAI)
*Send any prompt to any provider through a single unified endpoint.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Test Local Ollama:
```json
{
  "provider": "ollama",
  "model": "llama3.2",
  "prompt": "What is prompt caching in 2 sentences?"
}
```

#### B) Test Cloud OpenAI:
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "What is prompt caching in 2 sentences?"
}
```

---

### Week 2 • Day 1 • Test 3: Inference-Time Scaling (Reasoning Puzzle)
*Tests `gpt-5-nano` with variable `reasoning_effort` on a conditional probability puzzle.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### Test Minimal Reasoning (Fast / Heuristic):
- **Request Body**:
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only.",
  "reasoning_effort": "minimal"
}
```
- **Observed Result**: Returns `1/2` (Intuitive, fast heuristic mistake).

#### Test Low Reasoning (Calculated / Thinking Tokens):
- **Request Body**:
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only.",
  "reasoning_effort": "low"
}
```
- **Observed Result**: Returns `2/3` (Correct conditional probability over sample space `{HH, HT, TH}`).

---

### Week 2 • Day 1 • Test 4: Frontier Spatial Reasoning (Pushkin Bookworm Puzzle)
*Classic spatial puzzle that exposes the difference between surface pattern matching and frontier spatial comprehension.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Test with `gpt-5-nano` (Falls into the trap):
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "On a bookshelf, two volumes of Pushkin stand side by side: the first and the second. The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick. A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume. What distance did it gnaw through?",
  "reasoning_effort": "minimal"
}
```
- **Result**: `44 mm (4.4 cm)` *(Trapped! Assumed it had to gnaw through all pages of both volumes).*

#### B) Test with Frontier `gpt-5` (Solves the spatial trick):
```json
{
  "provider": "openai",
  "model": "gpt-5",
  "prompt": "On a bookshelf, two volumes of Pushkin stand side by side: the first and the second. The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick. A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume. What distance did it gnaw through?"
}
```
- **Result**: `4 mm (0.4 cm)` *(Correct! Volume 1's page 1 faces Volume 2, and Volume 2's last page faces Volume 1; only two covers separate them).*

---

### Week 2 • Day 1 • Test 5: Real-Time Token Streaming
*Returns an `HTTP 200` chunked text stream, yielding tokens word-by-word.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/stream`
- **Request Body**:
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "Write a 4-line poem about debugging code at midnight."
}
```

---

### Week 2 • Day 1 • Test 6: Model Latency & Token Benchmarking
*Runs a single prompt against multiple models in parallel or series and returns side-by-side execution latency and token metrics.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/benchmark`
- **Request Body**:
```json
{
  "prompt": "Why should companies run local AI models? Give 2 concise points.",
  "targets": [
    { "provider": "ollama", "model": "llama3.2" },
    { "provider": "openai", "model": "gpt-4o-mini" }
  ]
}
```
- **Expected Response**:
```json
{
  "status": "success",
  "prompt": "Why should companies run local AI models? Give 2 concise points.",
  "results": [
    {
      "target": "ollama (llama3.2)",
      "status": "success",
      "duration_seconds": 18.42,
      "tokens": 85,
      "response": "..."
    },
    {
      "target": "openai (gpt-4o-mini)",
      "status": "success",
      "duration_seconds": 2.15,
      "tokens": 78,
      "response": "..."
    }
  ]
}
```

---

### Week 2 • Day 1 • Test 7: Autonomous 2-Agent Debate
*Simulates multi-turn debate where Agent 1 and Agent 2 speak back-and-forth responding to each other's points.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/multi-agent/debate`
- **Request Body**:
```json
{
  "topic": "Will open source local models replace cloud APIs?",
  "rounds": 2,
  "agent_1": {
    "name": "Alex",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "personality": "You are a sharp technology skeptic who prioritizes cloud ecosystems and reliability."
  },
  "agent_2": {
    "name": "Blake",
    "provider": "ollama",
    "model": "llama3.2",
    "personality": "You are an open-source optimist who champions privacy and edge computing."
  }
}
```
- **Expected Response**:
```json
{
  "status": "success",
  "topic": "Will open source local models replace cloud APIs?",
  "rounds": 2,
  "transcript": [
    { "speaker": "Alex", "message": "..." },
    { "speaker": "Blake", "message": "..." },
    { "speaker": "Alex", "message": "..." },
    { "speaker": "Blake", "message": "..." }
  ]
}
```

---

### Week 2 • Day 1 • Test 8: 3-Way Multi-Agent Round Robin
*Simulates a collaborative 3-party panel where each agent contributes in rotation.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/multi-agent/three-way`
- **Request Body**:
```json
{
  "topic": "How will generative AI redefine software engineering over the next 5 years?",
  "rounds": 1
}
```

---

## ⚖️ Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework

*Architectural comparison between **LiteLLM** (Universal Model Gateway & Proxy) and **LangChain** (Application Orchestrator & LCEL Pipelines).*

---

### Week 2 • Day 1 • Test 9: LiteLLM Unified Gateway & Spend Tracking (Lec 42)
*Universal model gateway call supporting 100+ providers with latency and exact token/USD cost metrics.*

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

---

### Week 2 • Day 1 • Test 10: LangChain LCEL Declarative Pipeline (Lec 42)
*Multi-step sequential reasoning using `prompt \| model \| parser` chains (Step 1: Technical Analysis $\to$ Step 2: Executive Roadmap).*

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

---

### Week 2 • Day 1 • Test 11: LangChain vs LiteLLM Side-by-Side Comparison (Lec 42)
*Executes the same query through both frameworks concurrently and returns comparative latencies, token consumption, and architectural recommendations.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/compare`
- **Request Body**:
```json
{
  "prompt": "Explain database indexing to a junior backend developer in 2 sentences.",
  "model": "gpt-4o-mini"
}
```

---

### 💻 Week 2 Day 1 Standalone Terminal Runners
To run Week 2 Day 1 suites directly in terminal:

```powershell
# 1. Multi-Agent, Reasoning Models & Local Ollama
python week2/day1/practice.py

# 2. Lec 42: Day 1 — LangChain vs LiteLLM Comprehensive Suite
python week2/day1_langchain_vs_litellm.py

# 3. Baseline Hamlet & Token/Cost Check (Cells 59-62)
python week2/check_hamlet_gemini.py

# 4. LiteLLM Pro-Feature: Prompt Caching Walkthrough (Cells 63-67)
python week2/demo_prompt_caching.py

# 5. OpenAI Prompt Caching Deep-Dive (Prefix Matching & Thresholds)
python week2/demo_openai_prompt_caching.py
```

---

## 🎨 PREVIEW: WEEK 2 • DAY 2 ("Gradio Day!")
- **Theme**: Building Interactive User Interfaces with Gradio (Simple Chat, Custom Themes, Streaming).
- **Core Library**: `gradio>=6.30.0` (installed and configured in `.venv`).
- **Upcoming Milestone**: Creating interactive web UIs for your LLM agents and mounting Gradio into FastAPI.

