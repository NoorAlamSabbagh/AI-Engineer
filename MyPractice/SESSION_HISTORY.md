# 📝 Permanent Session History & Development Record
**Session Date:** October 11–12, 2026  
**Topic:** Setup & Implementation for **Lec 42: Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework**  
**Workspace:** `d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice`  

---

## 📌 Why This File Exists
Chat sessions in AI assistants can reset or clear between restarts. This file serves as a **permanent, version-controlled audit log** of everything investigated, installed, created, and verified during this session so you can pick up anytime without losing context.

---

## 🔍 1. Context & Objectives of This Session

1. **Course Context**:
   - Course: *AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents* by **Ed Donner**.
   - Section: **Week 2**.
   - Lecture: **Lec 42. Day 1 — LangChain vs LiteLLM: Choosing the Right LLM Framework**.
2. **Core Dilemma Taught in the Lecture**:
   - **LiteLLM**: The Universal Model Gateway & Proxy. Translates 100+ LLM APIs to the OpenAI `completion()` standard. Lightweight (~40MB), built-in spend tracking (`completion_cost`), streaming, and model fallbacks.
   - **LangChain**: The Application Orchestration Engine. Powered by LCEL (LangChain Expression Language: `prompt | model | parser`). Excels at multi-step reasoning, RAG (vector retrieval), and autonomous tool-calling agents.
   - **The Industry Hybrid Pattern**: Using LangChain for high-level workflow orchestration, while routing model calls through LiteLLM for universal provider access, retries, and rate limiting.

---

## 📦 2. Dependencies Installed & Configured

Installed into `MyPractice/.venv` and added to `MyPractice/requirements.txt`:
```txt
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
python-dotenv>=1.0.1
pydantic>=2.0.0
openai>=1.14.0
beautifulsoup4>=4.12.0
requests>=2.31.0
litellm>=1.77.0
langchain>=0.3.0
langchain-openai>=0.3.0
langchain-community>=0.3.0
langchain-core>=0.3.0
```

---

## 🛠️ 3. Architecture & Code Changes Created

### A. Standalone Terminal Script (Direct Lecture Flow)
- **File**: [`MyPractice/week2/day1_langchain_vs_litellm.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1_langchain_vs_litellm.py)
  - Every function and section is tagged `# [Lec 42: Day 1]`.
  - **Section 1**: `lec42_day1_demo_direct_sdk()` $\to$ Demonstrates raw OpenAI SDK and discusses vendor lock-in.
  - **Section 2**: `lec42_day1_demo_litellm()` $\to$ Demonstrates unified `completion()`, spend tracking with `completion_cost()`, provider swap (OpenAI $\to$ Groq/Ollama) with 0 code change, and streaming tokens.
  - **Section 3**: `lec42_day1_demo_langchain()` $\to$ Demonstrates LCEL pipe syntax (`prompt | model | parser`), 2-step sequential chain (Analysis $\to$ Action Roadmap), and token streaming via `chain.stream()`.
  - **Section 4**: `lec42_day1_print_decision_matrix()` $\to$ Outputs the complete architectural decision matrix.

### B. 4-Layer FastAPI Backend Integration
1. **Schemas** ([`src/schemas/frameworks.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/schemas/frameworks.py)):
   - `LiteLLMRequest`, `LangChainChainRequest`, `FrameworkCompareRequest`, `FrameworkCompareResponse`, `FrameworkMetric`.
2. **Service Layer** ([`src/services/framework_comparison.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/services/framework_comparison.py)):
   - `execute_litellm_query()`, `execute_langchain_chain()`, `compare_frameworks()`.
3. **Controller Layer** ([`src/controllers/frameworks.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/controllers/frameworks.py)):
   - `handle_litellm_query()`, `handle_langchain_chain()`, `handle_framework_compare()`.
4. **Route Layer** ([`src/routes/frameworks.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/routes/frameworks.py)):
   - `POST /frameworks/litellm`
   - `POST /frameworks/langchain`
   - `POST /frameworks/compare`
   - Tagged as `"Lec 42: Day 1 — LangChain vs LiteLLM"` for Swagger UI.
5. **Main Entrypoint** ([`src/main.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/main.py)):
   - Router imported and registered with explicit `[Lec 42: Day 1]` comments.

### C. Master Documentation & Trackers
1. [`MyPractice/COURSE_TRACKER.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/COURSE_TRACKER.md): Complete curriculum progression tracking from Week 1 to Week 8.
2. [`MyPractice/PRACTICE_SUMMARY.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/PRACTICE_SUMMARY.md): Master testing manual updated with Tests 9, 10, and 11.
3. [`MyPractice/week2/README.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/README.md): Week 2 directory roadmap.
4. [`MyPractice/week2/day1/LANGCHAIN_VS_LITELLM.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/LANGCHAIN_VS_LITELLM.md): Full deep-dive guide with architecture diagrams.

### D. Cleanup Actions
- Deleted duplicate clone: `MyPractice/week2/day1/langchain_vs_litellm.py`.
- Restored: `MyPractice/Day1/Notes.js` from git history to ensure past notes are retained.
- Verified all python files compiled cleanly with zero syntax errors.

---

## 🚀 4. How to Run Lec 42: Day 1 Right Now

### Option A: Run the Terminal Practice Script
Open your PowerShell terminal and run:

```powershell
# 1. Navigate to the MyPractice directory
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"

# 2. Activate Python virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Run the Lec 42 standalone script
python week2/day1_langchain_vs_litellm.py
```

### Option B: Test via FastAPI Server & Swagger UI
```powershell
# 1. From MyPractice with .venv active:
uvicorn src.main:app --reload
```
- Open your browser to: **`http://127.0.0.1:8000/docs`**
- Scroll down to the tag: **`Lec 42: Day 1 — LangChain vs LiteLLM`**
- Try out:
  - `POST /frameworks/litellm`
  - `POST /frameworks/langchain`
  - `POST /frameworks/compare`

### 11. Quick Reference: Token & Cost Breakdown Snippet (`Cell 58`)
- **Snippet**:
  ```python
  print(f"Input tokens: {response.usage.prompt_tokens}")
  print(f"Output tokens: {response.usage.completion_tokens}")
  print(f"Total tokens: {response.usage.total_tokens}")
  print(f"Total cost: {response._hidden_params['response_cost']*100:.4f} cents")
  ```
- **Course Origin**: [week2/day1.ipynb](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/llm_engineering-main/week2/day1.ipynb#L935-940) (`In [58]`), directly under `## Finally - my personal fave - the wonderfully lightweight LiteLLM`.
- **Practice Implementation**: Integrated in [MyPractice/week2/day1_langchain_vs_litellm.py](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1_langchain_vs_litellm.py#L105-118) and returned via FastAPI at `POST /frameworks/litellm` (field `cost_usd`).

### 12. LiteLLM Pro-Feature: Prompt Caching (`Cells 59-67`)
- **Objective**: Eliminate repeated costs for large static prompts (e.g., Hamlet ~40k tokens) by caching prefix tokens at the model provider level.
- **Dedicated Script**: [MyPractice/week2/demo_prompt_caching.py](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/demo_prompt_caching.py)
- **Document Asset**: [MyPractice/week2/hamlet.txt](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/hamlet.txt)
- **Key Metrics**:
  - `response.usage.prompt_tokens`: Total input tokens.
  - `response.usage.prompt_tokens_details.cached_tokens`: Number of tokens served from cache (discounted).
  - `response._hidden_params["response_cost"] * 100`: Total cost in cents (discounted on cache hit).

### 13. Dedicated PowerShell Execution Track Record
- A dedicated, copy-pasteable execution track record is maintained in:
  - Text format: [MyPractice/POWERSHELL_RUN_GUIDE.txt](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/POWERSHELL_RUN_GUIDE.txt)
  - Detailed summary of all 5 execution modes:
    1. Baseline Hamlet & Token/Cost Check (`check_hamlet_gemini.py`)
    2. Prompt Caching Walkthrough (`demo_prompt_caching.py`)
    3. Full Framework Comparison Runner (`day1_langchain_vs_litellm.py`)
    4. FastAPI Swagger UI API (`uvicorn src.main:app --reload`)
    5. Regression Unit Test Suite (`practice.py`)

### 14. OpenAI Prompt Caching Deep-Dive (`Markdown Cell 68`)
- **Objective**: Verify the 4 core rules of OpenAI prompt caching (threshold, prefix match, zero-config, 4x discount).
- **Dedicated Script**: [MyPractice/week2/demo_openai_prompt_caching.py](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/demo_openai_prompt_caching.py)
- **Verified Findings**:
  - Test 1: Short prompts (<1,024 tokens) return `cached_tokens = 0`.
  - Test 2: Request 1 primes the cache (`cached_tokens = 0`, cost: `0.0793 cents`).
  - Test 3: Request 2 hits the cache with exact prefix match (`cached_tokens = 5,120`, cost: `0.0403 cents`, **49.2% discount**).

### 15. Week 2 Day 2: Gradio Web User Interfaces & Real-Time Streaming (Lec 44–48)
- **Topic**: Building Interactive User Interfaces with Gradio (`gr.Interface`, `gr.Blocks`, `gr.TabbedInterface`).
- **Lecture Range**: **Lectures 44 to 48** (Course syllabus: Gradio Day).
- **Modules Created in `MyPractice/week2/day2/`**:
  1. [`01_gradio_basics.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/01_gradio_basics.py): Python functions to UI components (`fn`, `inputs`, `outputs`), text transforms, input styling.
  2. [`02_llm_streaming.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/02_llm_streaming.py): Real-time token streaming using Python generators (`yield`), model switcher (OpenAI & Ollama).
  3. [`03_brochure_generator.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/03_brochure_generator.py): Day 2 Capstone — Web scraping (BeautifulSoup) + live streaming Markdown executive company brochure generator.
  4. [`04_full_dashboard.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/04_full_dashboard.py): All-in-one multi-tab Gradio dashboard running all 3 labs simultaneously.
  5. [`scraper.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/scraper.py): Self-contained web content scraper with sanitization.
  6. [`README.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day2/README.md): Step-by-step beginner guide with exact PowerShell execution commands.

### 16. Week 2 Day 3: Building Chat UIs with Gradio (Lec 49–52)
- **Topic**: Conversational AI Assistants & Multi-Turn State (`gr.ChatInterface`).
- **Lecture Range**: **Lectures 49 to 52** (`day3.ipynb`).
- **Modules Created in `MyPractice/week2/day3/`**:
  1. [`README.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day3/README.md): Beginner guide with layman analogies (the Goldfish Memory of LLMs, the Memory Sandwich, streaming).
  2. [`practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day3/practice.py): Single master file containing all 4 labs:
     - **Lab 1**: `gr.ChatInterface` callback mechanics and history inspection.
     - **Lab 2**: Memory Sandwich multi-turn chat with `gpt-4o-mini`.
     - **Lab 3**: Real-time typewriter token streaming (`yield`).
     - **Lab 4 (Capstone)**: Clothing store sales assistant with 60% off hats, 50% off other items, shoe guardrail, and dynamic belt injection.

### 17. Week 2 Day 4: How LLM Tool Calling Really Works (Lec 53–56)
- **Topic**: Function / Tool Calling Architecture, Handshakes, Parallel Tools, SQLite DB & Autonomous Agents.
- **Lecture Range**: **Lectures 53 to 56** (`day4.ipynb`).
- **Modules Created in `MyPractice/week2/day4/`**:
  1. [`README.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day4/README.md): Step-by-step conceptual guide explaining why tool calling is "No Magic, Just Prompts" with sequence diagrams.
  2. [`practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day4/practice.py): Single master file containing all 4 labs:
     - **Tab 1**: Baseline Airline Assistant (no tools) demonstrating model limitations.
     - **Tab 2**: In-Memory tool calling with single and parallel multi-city queries.
     - **Tab 3**: Live SQLite database queries (`SELECT`) and price updates (`UPDATE`) with live table inspector.
     - **Tab 4 (Capstone)**: Autonomous multi-step Airline Agent powered by a `while` loop inside `gr.ChatInterface`.
  3. `prices.db`: Auto-initialized SQLite database storing persistent flight fares.

### 18. Week 2 Day 5: Agentic AI, Multi-Tool Workflows & Frontier SVG Revealer (Lec 57–61)
- **Topic**: Agentic AI Foundations, Gradio Hierarchy (`gr.Interface` vs `gr.ChatInterface` vs `gr.Blocks`), Event Pipelines (`.then()`), Multi-Modal Workflows, and Frontier SVG AI Benchmark.
- **Lecture Range**: **Lectures 57 to 61** (`day5.ipynb` & `extra.ipynb`).
- **Modules Created in `MyPractice/week2/day5/`**:
  1. [`README.md`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day5/README.md): Layman guide explaining Agentic AI (the Butler vs the Calculator), Gradio UI Hierarchy, the FlightAI Multimodal pipeline, and Simon Willison's SVG benchmark.
  2. [`revealer.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day5/revealer.py): SVG XML parser and `@keyframes reveal` CSS injector providing staggered, animated vector drawing in the browser.
  3. [`practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day5/practice.py): Master 5-tab Gradio app:
     - **Tab 1 (Lec 57)**: Gradio UI Hierarchy comparison matrix.
     - **Tab 2 (Lec 58)**: Standalone multi-modal generators: `artist(city)` (DALL-E pop-art with PIL fallback) and `talker(text)` (OpenAI TTS audio).
     - **Tab 3 (Lec 59)**: Autonomous Multi-Tool Workflow coordinating SQLite tool calls and destination city extraction.
     - **Tab 4 (Lec 60 Capstone)**: FlightAI Grand Capstone — custom `gr.Blocks` dashboard with side-by-side Chatbot, dynamic pop-art postcard preview, autoplaying TTS audio, and `.then()` event chaining.
     - **Tab 5 (Lec 61 Special Extra)**: Frontier SVG Artist & Animated Revealer featuring Simon Willison's pelican and course panda benchmarks with live keyframe animation.
  4. `prices.db`: Auto-initialized persistent SQLite database for flight queries and updates.

