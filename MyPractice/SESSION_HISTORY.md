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

### 15. Transition: Week 2 Day 2 Readiness ("Gradio Day!")
- **Topic**: Building Interactive User Interfaces with Gradio (Simple Chat, Streaming, Themes, LLM integrations).
- **Dependencies Installed**:
  - `gradio>=6.30.0` installed into `.venv`.
  - Updated [MyPractice/requirements.txt](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/requirements.txt).
- **Course Notebook**: [llm_engineering-main/week2/day2.ipynb](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/llm_engineering-main/week2/day2.ipynb).
- **Next Practice Target**: Create `MyPractice/week2/day2/` practice modules, standalone Gradio apps (`app.py`), and FastAPI mounting.




