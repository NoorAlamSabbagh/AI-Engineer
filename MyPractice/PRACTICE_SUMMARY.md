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

## 🎨 WEEK 2 • DAY 2: Gradio Web User Interfaces & AI Frontends (Lec 44–48)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week2/day2/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/README.md)
- **Core Concepts**: `gr.Interface`, `gr.Blocks`, `gr.TabbedInterface`, real-time token streaming (`yield`), HTML scraping + AI brochure generation.

### 💻 Week 2 Day 2 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Gradio Master Suite (Lec 44–48, Port 7860)
python week2/day2/practice.py
```

---

### 🧪 FastAPI Swagger UI Tests for Day 2 (Lec 44–48)
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **FastAPI-Mounted Gradio Web App**: [http://127.0.0.1:8000/gradio](http://127.0.0.1:8000/gradio)

---

### Week 2 • Day 2 • Test 12: Gradio Mounted UI Discovery (Lec 44–48)
*Discovers the status, mounted route, and interactive tabs of the Gradio interface mounted on FastAPI.*

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/ui/info`
- **Headers**: *(None)*
- **Expected Response**:
```json
{
  "status": "active",
  "lecture_range": "Lec 44–48",
  "mounted_path": "/gradio",
  "browser_url": "http://127.0.0.1:8000/gradio",
  "available_tabs": [
    "Tab 1: 🚀 Gradio 101 Basics (Lec 44 & 45)",
    "Tab 2: ⚡ Real-Time LLM Token Streaming (Lec 46 & 47)",
    "Tab 3: 🏢 AI Company Brochure Generator (Lec 48 Capstone)"
  ],
  "supported_models": [
    "OpenAI (gpt-4o-mini)",
    "Local Ollama (llama3.2)"
  ]
}
```

---

### Week 2 • Day 2 • Test 13: Functional Text Transformation (Lec 44–45)
*API backend version of the Gradio Tab 1 transformation functions.*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/ui/transform`
- **Request Body**:
```json
{
  "text": "Artificial Intelligence Engineering is Transforming Tech",
  "mode": "SHOUT (Uppercase)"
}
```
- **Alternate modes**: `"whisper (lowercase)"`, `"Reverse Text"`, `"Word & Character Count"`

---

### Week 2 • Day 2 • Test 14: Web Scraper & Executive Brochure Generator (Lec 48 Capstone)
*API backend version of the Gradio Tab 3 brochure generator (live website scrape + LLM).*

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/ui/brochure`
- **Request Body**:
```json
{
  "company_name": "Hugging Face",
  "url": "https://huggingface.co",
  "model": "gpt-4o-mini"
}
```
- **Response**: Returns `scraped_characters` and structured `brochure_markdown` containing Executive Overview, Problem & Value Proposition, Flagship Products, Target Market, and Next Steps.

---

## 💬 WEEK 2 • DAY 3: Building Chat UIs with Gradio (Lec 49–52)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week2/day3/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day3/README.md)
- **Core Concepts**: `gr.ChatInterface`, callback structure `(message, history)`, the "Memory Sandwich" formula, real-time token streaming (`yield`), and retail sales assistant persona with dynamic guardrails.

### 💻 Week 2 Day 3 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Conversational AI Dashboard (Lec 49–52, Port 7860)
python week2/day3/practice.py
```

### 🧪 Labs Included in `week2/day3/practice.py`:
1. **Lab 1: Chatbot 101 Basics** — Explores `(message, history)` plumbing and turn counter.
2. **Lab 2: Multi-Turn Memory Chat** — Bundles history into OpenAI API calls so context is preserved.
3. **Lab 3: Live Token Streaming** — Typewriter live text streaming in chat bubbles via `yield`.
4. **Lab 4: Clothing Store Sales Assistant (Capstone)** — Persona with 60% off hats, 50% off other items, shoe guardrail, and dynamic out-of-stock injection for belts.

---

## 🛠️ WEEK 2 • DAY 4: How LLM Tool Calling Really Works (Lec 53–56)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week2/day4/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day4/README.md)
- **Core Concepts**: Demystifying tool calling ("No Magic, Just Prompts!"), JSON Schema function definitions, the 4-step tool handshake (`finish_reason == 'tool_calls'`), parallel multi-tool execution, persistent SQLite database integration (`prices.db`), and autonomous multi-step reasoning (`while` loop).

### 💻 Week 2 Day 4 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Tool Calling & Airline Agent Dashboard (Lec 53–56, Port 7860)
python week2/day4/practice.py
```

### 🧪 Labs Included in `week2/day4/practice.py`:
1. **Tab 1: Baseline Airline Assistant (Lec 53 — No Tools)** — Demonstrates model limitations and hallucinations when asked for live ticket prices without tools.
2. **Tab 2: In-Memory Tool Calling (Lec 54 — Parallel Calls)** — Tests JSON schema execution and parallel queries (e.g. comparing London, Paris, and Tokyo in one message).
3. **Tab 3: SQLite Database Tools (Lec 55 — Read & Write)** — Real SQLite table queries (`SELECT`) and fare updates (`UPDATE`) with live table view.
4. **Tab 4: Autonomous Airline Agent (Lec 56 Capstone)** — Multi-step `while` loop agent capable of complex reasoning, multi-city comparisons, and database updates inside `gr.ChatInterface`.

---

## 🤖 WEEK 2 • DAY 5: Introduction to Agentic AI & Building Multi-Tool Workflows (Lec 57–61)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week2/day5/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day5/README.md)
- **Core Concepts**: What makes an AI "Agentic" (autonomous goal achievement vs passive chatbot), Gradio UI Hierarchy (`gr.Interface` vs `gr.ChatInterface` vs `gr.Blocks`), Multi-Modal Tool Handshake (Text + SQLite + DALL-E / PIL Pop-Art Postcards + OpenAI TTS Audio), Event Chaining with `.then()`, FlightAI Multimodal Capstone, and Simon Willison's Frontier SVG AI Benchmark with animated CSS keyframe revealer (`revealer.py`).

### 💻 Week 2 Day 5 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Agentic AI & Multi-Tool Dashboard (Lec 57–61, Port 7860)
python week2/day5/practice.py
```

### 🧪 Labs Included in `week2/day5/practice.py`:
1. **Tab 1: Gradio UI Hierarchy Comparison (Lec 57)** — Architectural breakdown comparing `gr.Interface` (pure I/O function), `gr.ChatInterface` (conversational history wrapper), and `gr.Blocks` (fine-grained bespoke canvas).
2. **Tab 2: Multi-Modal Tools: Artist & Talker (Lec 58)** — Standalone generators for image generation (`artist(city)` creating pop-art travel postcards via DALL-E with local PIL fallback) and speech synthesis (`talker(text)` via OpenAI TTS `alloy` voice).
3. **Tab 3: Agentic Multi-Tool Workflow (Lec 59)** — Autonomous reasoning engine that combines SQLite queries with destination extraction and multi-modal tool dispatching.
4. **Tab 4: FlightAI Grand Capstone (Lec 60)** — Full-featured travel assistant featuring side-by-side Chatbot and Destination Postcard preview, autoplaying Audio advice, and event chaining with `.then()`.
5. **Tab 5: Special Extra: Frontier SVG Artist & Revealer (Lec 61)** — Simon Willison's SVG benchmark ("pelican riding a bicycle" / "panda rollerblading to work") evaluating spatial reasoning and vector coordinate math, paired with an animated SVG keyframe revealer (`revealer.py`).

---

## 🚀 WEEK 3 • DAY 1: Google Colab, Cloud GPUs & Open-Source Generative AI (Lec 62–67)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week3/day1/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day1/README.md)
- **Core Concepts**: Cloud GPU compute on Google Colab (Tesla T4 vs A100), Hugging Face Hub write access authentication (`HF_TOKEN`), Fast Latent Diffusion (SDXL-Turbo in 1–4 steps), 2-Stage Denoising Ensemble (Base 80% + Refiner 20%), Neural Text-to-Speech with Speaker Embeddings (SpeechT5 + CMU Arctic x-vectors), and Frontier FLUX.1-schnell cloud cost economics.

### 💻 Week 3 Day 1 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Open-Source Models & Cloud GPU Dashboard (Lec 62–67, Port 7860)
python week3/day1/practice.py
```

### 🧪 Labs Included in `week3/day1/practice.py`:
1. **Tab 1: Cloud GPU & HF Inspector (Lec 62–63)** — Diagnostic scanner testing PyTorch, CUDA devices, VRAM allocations, `nvidia-smi` binary output, and Hugging Face Hub Write token credentials.
2. **Tab 2: Fast Latent Diffusion Studio (Lec 64)** — Lightning-fast 1 to 4 step image synthesis using `stabilityai/sdxl-turbo` with `guidance_scale=0.0`.
3. **Tab 3: Two-Stage Diffusion Pipeline (Lec 65)** — Ensemble pipeline combining coarse composition (`sdxl-base-1.0`) and fine detail refinement (`sdxl-refiner-1.0`) with interactive split fractions.
4. **Tab 4: Neural Text-to-Speech (Lec 66)** — Voice generation via `microsoft/speecht5_tts` utilizing customizable 512-dimensional speaker embeddings.
5. **Tab 5: Frontier FLUX & GPU Economics Calculator (Lec 67)** — Interactive cloud cost calculator modeling active compute vs expensive idle runtime leakage on NVIDIA T4 and A100 instances.

### ☁️ Standalone Google Colab Notebook:
- [`colab_notebook.ipynb`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day1/colab_notebook.ipynb): Direct uploadable notebook containing every single execution cell from Ed's lecture, preconfigured for Google Colab's free T4 GPU tier.

---

## 🚀 WEEK 3 • DAY 2: Hugging Face Pipelines for Quick AI Inference (Lec 68–71)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week3/day2/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day2/README.md)
- **Core Concepts**: Hugging Face High-Level Pipelines (`pipeline()`), Training vs. Inference distinction, Sentiment Analysis (Binary vs. Multilingual 5-Star), Named Entity Recognition (NER), Contextual Question Answering, Text Summarization, Machine Translation (Opus-MT French & Spanish), Zero-Shot NLI Classification, Causal Text Generation, and Multi-Modal Pipelines (Image Diffusion & Neural TTS).

### 💻 Week 3 Day 2 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Hugging Face Pipelines Suite (Lec 68–71, Port 7861)
python week3/day2/practice.py
```

### 🧪 Labs Included in `week3/day2/practice.py`:
1. **Tab 1: Pipeline Architecture (Lec 68)** — Interactive device scanner and architectural breakdown comparing Training ($\Delta \theta$ backpropagation) vs Inference (frozen forward pass).
2. **Tab 2: Core Text NLP Studio (Lec 69)** — Interactive Sentiment Analysis (DistilBERT vs BERT 5-Star), Named Entity Recognition (`ner`), and Extractive Question Answering (`question-answering`).
3. **Tab 3: Sequence-to-Sequence & Zero-Shot (Lec 70)** — Text Summarization with length sliders, Opus-MT translation (English $\to$ French & Spanish), Zero-Shot dynamic categorization, and Causal Text Generation.
4. **Tab 4: Multi-Modal Diffusion & Speech Studio (Lec 71)** — Latent Image Generation (`sdxl-turbo`) and Speech Synthesis (`speecht5_tts`).

### ☁️ Standalone Google Colab Notebooks:
- [`day2_colab_original.ipynb`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day2/day2_colab_original.ipynb): 100% Verbatim clone extracted directly from Ed's Google Drive (`1aMaEw8A56xs0bRM4lu8z7ou18jqyybGm`).
- [`colab_notebook.ipynb`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day2/colab_notebook.ipynb): Annotated edition with clean lecture boundaries (Lec 68 to 71).

---

## 🧩 WEEK 3 • DAY 3: Tokenizers & Chat Templates Master Suite (Lec 72–75)
- **Status**: 🟢 **Ready for Practice**
- **Folder**: [`MyPractice/week3/day3/`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day3/README.md)
- **Core Concepts**: Byte-Pair Encoding (BPE), Characters vs Words vs Tokens, Vocabulary sizes (`len(tokenizer.vocab)`), Special delimiter tokens, The Crucial "Aha!" Moment (Why LLMs can't accept Python dicts), `apply_chat_template()`, and Cross-Model Tokenizer Benchmarks (Meta Llama 3.1 8B, Microsoft Phi-4, DeepSeek V3, and Alibaba Qwen 2.5 Coder).

### 💻 Week 3 Day 3 Terminal Runner (PowerShell)

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Launch the Unified Tokenizer & Chat Template Dashboard (Lec 72–75, Port 7862)
python week3/day3/practice.py
```

### 🧪 Labs Included in `week3/day3/practice.py`:
1. **Tab 1: Tokenizer Foundations (Lec 72)** — Real-time text analyzer comparing Character count, Word count, and Token count with compression ratios; alternating color pill chips for subword visual inspection; detailed Token ID inspection table.
2. **Tab 2: The Chat Template "Aha!" Moment (Lec 73–74)** — Interactive prompt builder demonstrating how structured Python `messages` lists get formatted into raw string sequences with model-specific delimiters (`<|start_header_id|>...`, `<|im_start|>...`, `<｜User｜>...`); toggling `add_generation_prompt=True` to inspect the assistant response cue.
3. **Tab 3: Comparing Frontier Tokenizers (Lec 75)** — Side-by-side benchmark across Meta Llama 3.1 (128k vocab), Microsoft Phi-4 (100k vocab), DeepSeek V3 (129k vocab), and Alibaba Qwen 2.5 Coder (152k vocab); includes Python code indentation tests demonstrating Qwen-Coder's single-token indent superpowers.
4. **Tab 4: Token Probability & Prediction Visualizer (Ed's visualizer.py)** — Token-by-token branching tree displaying top chosen tokens alongside runner-up alternatives and percentage confidence probabilities; interactive temperature slider testing greedy vs stochastic decoding.

### ☁️ Standalone Google Colab Notebooks:
- [`day3_colab_original.ipynb`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day3/day3_colab_original.ipynb): 100% Verbatim clone extracted directly from Ed's Google Drive (`1WD6Y2N7ctQi1X9wa6rpkg8UfyA4iSVuz`).
- [`colab_notebook.ipynb`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week3/day3/colab_notebook.ipynb): Annotated edition with clean lecture boundaries (Lec 72 to 75).

