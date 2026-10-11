# 📁 Week 2 — Advanced LLM Engineering, Local Models & Multi-Agent Architecture

Welcome to **Week 2**! This directory contains all day-by-day practice and implementations for Week 2.

---

## 🗂️ Week 2 Day 1 Functionality Map

| Part | Topic / Concept | File | Primary Function(s) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Part 1** | **Hamlet Baseline & Cost Metrics** | [`check_hamlet_gemini.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/check_hamlet_gemini.py) | `run_check()` | Verifies `hamlet.txt`, runs baseline query without context, prints tokens and cost in cents. |
| **Part 2** | **LiteLLM Pro-Feature: Prompt Caching** | [`demo_prompt_caching.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/demo_prompt_caching.py) | `lec42_day1_prompt_caching_demo()` | Attaches 40k tokens of Hamlet; compares Cold Call vs Warm Call (reusing 49,536 cached tokens at 50% discount). |
| **Part 3** | **LangChain vs LiteLLM Comparison** | [`day1_langchain_vs_litellm.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1_langchain_vs_litellm.py) | `lec42_day1_demo_direct_sdk()`<br>`lec42_day1_demo_litellm()`<br>`lec42_day1_demo_langchain()`<br>`lec42_day1_print_decision_matrix()` | Full lecture walkthrough: Direct SDK vs LiteLLM Gateway vs LangChain LCEL 2-step chain vs Decision Matrix. |
| **Part 4** | **Production 4-Layer API** | [`src/routes/frameworks.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/routes/frameworks.py) | `compare_frameworks_service()`<br>`run_litellm_gateway_service()`<br>`run_langchain_pipeline_service()` | FastAPI REST endpoints tagged under `"Lec 42: Day 1"` for Swagger UI testing. |
| **Part 5** | **Week 2 Day 1 Test Suite** | [`week2/day1/practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/practice.py) | `test_frontier_models()`<br>`test_system_prompting()`<br>`test_framework_comparison()` | Automated unit test suite verifying all 6 curriculum modules pass. |

---

## 🚀 PowerShell Execution Cheatsheet

```powershell
# 1. Baseline Hamlet & Token/Cost Check (Cells 59-62)
& "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\.venv\Scripts\python.exe" "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\week2\check_hamlet_gemini.py"

# 2. LiteLLM Prompt Caching Walkthrough (Cells 63-67)
& "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\.venv\Scripts\python.exe" "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\week2\demo_prompt_caching.py"

# 3. Full LangChain vs LiteLLM Script (Lec 42 Runner)
& "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\.venv\Scripts\python.exe" "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\week2\day1_langchain_vs_litellm.py"

# 4. Interactive Swagger UI Backend
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\uvicorn.exe src.main:app --reload
# Open: http://127.0.0.1:8000/docs

# 5. Automated Regression Test Suite
& "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\.venv\Scripts\python.exe" "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice\week2\day1\practice.py"
```

For the complete standalone reference guide, open:
📄 [**`MyPractice/POWERSHELL_RUN_GUIDE.txt`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/POWERSHELL_RUN_GUIDE.txt)
