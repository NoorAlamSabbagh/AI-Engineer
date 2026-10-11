# 📁 Week 2 • Day 1 — Frontier APIs, Local Models, Reasoning & Multi-Agent Dialogue

Comprehensive API and terminal testing guide for **Week 2 Day 1**.

---

## ⚡ Server Startup

Ensure your FastAPI server is running:
```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Standard Header for all POST requests**: `Content-Type: application/json`

---

## 🧪 Test Suite Summary (Day 1)

| Test # | Topic | Method | Endpoint URL | Key Feature |
| :---: | :--- | :---: | :--- | :--- |
| **1** | Provider Discovery | `GET` | `/models/providers` | Lists Ollama local models & Cloud APIs |
| **2** | Unified Model Query | `POST` | `/models/query` | Switch between Ollama, OpenAI, Groq |
| **3** | Inference-Time Scaling | `POST` | `/models/query` | `gpt-5-nano` with `reasoning_effort` |
| **4** | Frontier Spatial Reasoning | `POST` | `/models/query` | Pushkin puzzle: `gpt-5-nano` vs `gpt-5` |
| **5** | Competitive Game Theory | `POST` | `/models/query` | Split or Steal: `gpt-4o-mini` vs `gpt-5-nano` |
| **6** | Real-Time Token Streaming | `POST` | `/models/stream` | Word-by-word streaming HTTP response |
| **7** | Side-by-Side Benchmark | `POST` | `/models/benchmark` | Latency and token usage comparison |
| **8** | Autonomous 2-Agent Debate | `POST` | `/multi-agent/debate` | 2-persona back-and-forth debate |
| **9** | 3-Way Round Robin Dialogue | `POST` | `/multi-agent/three-way` | Group 3-agent rotating dialogue |
| **10** | **LiteLLM Unified Gateway** | `POST` | `/frameworks/litellm` | Universal model calls with cost tracking |
| **11** | **LangChain LCEL Pipeline** | `POST` | `/frameworks/langchain` | Declarative `prompt \| model \| parser` chains |
| **12** | **LangChain vs LiteLLM Head-to-Head** | `POST` | `/frameworks/compare` | Direct comparison and decision matrix |

---

## 🔍 Detailed Tests & Request Payloads

---

### Test 1: Provider & Local Model Discovery
*Detects local Ollama instance (`llama3.2`, `deepseek-r1`, etc.) and cloud status.*

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/models/providers`
- **Headers**: *(None required)*
- **Body**: *(Empty)*
- **Expected Response**:
```json
{
  "status": "success",
  "providers": {
    "ollama": {
      "available": true,
      "type": "local",
      "endpoint": "http://localhost:11434/v1",
      "installed_models": ["llama3.2:latest", "gpt-oss:20b", "deepseek-r1:1.5b", "phi3:latest", "qwen3:4b"],
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

### Test 2: Unified Query (Local Ollama vs Cloud OpenAI)
*Send any prompt to any provider using the same schema.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Query Local Ollama:
```json
{
  "provider": "ollama",
  "model": "llama3.2",
  "prompt": "What is prompt caching in 2 sentences?"
}
```

#### B) Query Cloud OpenAI:
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "What is prompt caching in 2 sentences?"
}
```

---

### Test 3: Inference-Time Scaling (Reasoning Puzzle)
*Tests `gpt-5-nano` with variable `reasoning_effort` on conditional probability.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Minimal Reasoning (Fast / Heuristic mistake):
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only.",
  "reasoning_effort": "minimal"
}
```
- **Observed Output**: `1/2` *(Naive answer without deep calculation)*

#### B) Low Reasoning (Calculated thinking tokens):
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only.",
  "reasoning_effort": "low"
}
```
- **Observed Output**: `2/3` *(Correct conditional probability: sample space {HH, HT, TH})*

---

### Test 4: Frontier Spatial Reasoning (Pushkin Bookworm Puzzle)
*Tests spatial comprehension where naive addition fails.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Test with `gpt-5-nano` (Minimal Reasoning — Trapped):
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "On a bookshelf, two volumes of Pushkin stand side by side: the first and the second. The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick. A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume. What distance did it gnaw through?",
  "reasoning_effort": "minimal"
}
```
- **Observed Output**: `44 mm (4.4 cm)` *(Trapped! Blindly added all pages of both volumes)*

#### B) Test with Frontier `gpt-5` (Solves the spatial trick):
```json
{
  "provider": "openai",
  "model": "gpt-5",
  "prompt": "On a bookshelf, two volumes of Pushkin stand side by side: the first and the second. The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick. A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume. What distance did it gnaw through?"
}
```
- **Observed Output**: `4 mm (0.4 cm)` *(Correct! Volume 1 page 1 and Volume 2 last page are separated only by two covers)*

---

### Test 5: A Spicy Challenge to Test the Competitive Spirit (Split or Steal Dilemma)
*Game-theoretic Prisoner's Dilemma comparing cooperative vs game-theoretic Nash equilibrium decisions.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/query`

#### A) Test with `gpt-4o-mini` (Cooperative / Pro-social bias):
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:\nCooperate: Choose \"Share\" — if both of you choose this, you each win $1,000.\nDefect: Choose \"Steal\" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.\nIf both steal, you both get nothing.\nDo you choose to Steal or Share? Pick one."
}
```
- **Observed Output**: Chooses **"Share"** *(cooperative instinct).*

#### B) Test with Reasoning `gpt-5-nano` (Strict Game Theory Dominance):
```json
{
  "provider": "openai",
  "model": "gpt-5-nano",
  "prompt": "You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:\nCooperate: Choose \"Share\" — if both of you choose this, you each win $1,000.\nDefect: Choose \"Steal\" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.\nIf both steal, you both get nothing.\nDo you choose to Steal or Share? Pick one.",
  "reasoning_effort": "low"
}
```
- **Observed Output**: Chooses **"Steal"** *(mathematical dominance in single-shot Prisoner's Dilemma).*

---

### Test 6: Real-time Token Streaming
*Returns an `HTTP 200` chunked text stream, yielding tokens word-by-word.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/models/stream`
- **Request Body**:
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "Write a 4-line poem about late night coding."
}
```

---

### Test 7: Model Latency & Token Benchmarking
*Runs a single prompt against multiple models and returns execution latency and token metrics.*

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

### Test 8: Autonomous 2-Agent Debate
*Simulates multi-round back-and-forth debate between two personas.*

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
    "personality": "You are a skeptic who questions edge scalability and supports cloud infrastructure."
  },
  "agent_2": {
    "name": "Blake",
    "provider": "ollama",
    "model": "llama3.2",
    "personality": "You are a diplomat and open-source enthusiast promoting local models and data privacy."
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

### Test 9: 3-Way Multi-Agent Round Robin Dialogue
*Simulates a 3-agent group conversation where each speaker builds on the previous one.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/multi-agent/three-way`
- **Request Body**:
```json
{
  "topic": "How will AI change the day-to-day work of software engineers?",
  "rounds": 1
}
```

---

---

## 🦙 Going Local with Ollama — Step-by-Step Guide

You already have Ollama installed with the following models ready:
- `llama3.2:latest` (Default lightweight local model)
- `gpt-oss:20b` (Large local model)
- `deepseek-r1:1.5b` (Local reasoning model)
- `phi3:latest` (Microsoft 3.8B model)
- `qwen3:4b` (Alibaba 4B model)

---

### Step 1: Check If Ollama Daemon Is Running

In your PowerShell / terminal:
```powershell
ollama list
```
Or check via HTTP:
```powershell
curl http://localhost:11434
```
> If you see `Ollama is running`, your daemon is active!  
> If not running, start it by running `ollama serve` or opening the Ollama desktop app.

---

### Step 2: Test Local Inference in Python (OpenAI Universal Client)

The core principle of Week 2 Day 1 is using the **Universal OpenAI Client** to talk to Ollama without needing any separate library:

```python
from openai import OpenAI

# Point client directly to your local Ollama port
ollama = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" # required dummy string
)

response = ollama.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explain prompt caching in one sentence."}]
)

print(response.choices[0].message.content)
```

**Quick 1-Liner to run in terminal:**
```powershell
python -c "from openai import OpenAI; c = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama'); print(c.chat.completions.create(model='llama3.2', messages=[{'role': 'user', 'content': 'Hello from local Ollama!'}]).choices[0].message.content)"
```

---

### Step 3: Test Local Ollama in Swagger UI / Postman

With your FastAPI server running (`uvicorn src.main:app --reload`), open **`http://127.0.0.1:8000/docs`**:

#### 1. Query Local Model:
- **Endpoint**: `POST /models/query`
- **Body**:
```json
{
  "provider": "ollama",
  "model": "llama3.2",
  "prompt": "What are the advantages of running models locally on your own machine?"
}
```

#### 2. Test Local Real-Time Streaming:
- **Endpoint**: `POST /models/stream`
- **Body**:
```json
{
  "provider": "ollama",
  "model": "llama3.2",
  "prompt": "Count from 1 to 10 with words."
}
```

#### 3. Benchmark Local Ollama vs Cloud OpenAI:
- **Endpoint**: `POST /models/benchmark`
- **Body**:
```json
{
  "prompt": "What is overfitting?",
  "targets": [
    {"provider": "ollama", "model": "llama3.2"},
    {"provider": "openai", "model": "gpt-4o-mini"}
  ]
}
```

---

## ⚖️ Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework

*Hands-on framework evaluation: Unified I/O gateway (`LiteLLM`) vs declaratively composed reasoning pipelines (`LangChain LCEL`).*

For full architectural notes and decision matrix, see: 👉 [**`LANGCHAIN_VS_LITELLM.md`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/LANGCHAIN_VS_LITELLM.md)

---

### Test 10: LiteLLM Unified Model Gateway (Lec 42)
*Calls any LLM provider (OpenAI, Anthropic, Ollama, Groq) using a unified format, returning latency, token counts, and USD cost.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/litellm`
- **Body**:
```json
{
  "prompt": "What are the 3 golden rules of production LLM system design?",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}
```

---

### Test 11: LangChain LCEL Pipeline & Sequential Reasoning (Lec 42)
*Executes a composable LCEL chain (`ChatPromptTemplate \| ChatOpenAI \| StrOutputParser`) with two-step sequential reasoning.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/langchain`
- **Body**:
```json
{
  "topic": "Migrating from Monolith to Event-Driven Microservices",
  "target_audience": "VP of Engineering",
  "chain_type": "two_step"
}
```

---

### Test 12: LangChain vs LiteLLM Head-to-Head Comparison (Lec 42)
*Runs the exact same prompt through both frameworks concurrently and outputs side-by-side performance and recommendations.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/frameworks/compare`
- **Body**:
```json
{
  "prompt": "Explain database indexing to a junior backend developer in 2 sentences.",
  "model": "gpt-4o-mini"
}
```

---

## 💻 Standalone Terminal Runners

### 1. Multi-Agent & Frontier Models Suite:
```powershell
python week2/day1/practice.py
```

### 2. Lec 42: Day 1 — LangChain vs LiteLLM Comprehensive Suite:
```powershell
python week2/day1_langchain_vs_litellm.py
```

For complete architectural notes, pros/cons, and the Decision Tree, see:
👉 [**`week2/day1/LANGCHAIN_VS_LITELLM.md`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/LANGCHAIN_VS_LITELLM.md)

