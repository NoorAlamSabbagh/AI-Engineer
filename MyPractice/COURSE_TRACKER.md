# 🗺️ Master Course Tracker & Lecture Record
### **AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents**
*Instructor: Ed Donner | Repository: `MyPractice/`*

> 📌 **Looking for the permanent record of everything set up across chats?**  
> See the complete audit log: [**`SESSION_HISTORY.md`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/SESSION_HISTORY.md)

---

## 📊 Quick Progress Dashboard

| Week | Focus Area | Status | Practice Code / Files | Endpoints / Ports |
| :---: | :--- | :---: | :--- | :--- |
| **Week 1** | Foundations of LLMs & Web Intelligence | ✅ **Completed** | `week1/day1_intro.py` through `day5_brochure.py` | `POST /ask`, `POST /website/*` |
| **Week 2 (Day 1 Part 1)** | Frontier APIs, Local Ollama, Reasoning & Agents | ✅ **Completed** | `week2/day1/practice.py` | `POST /models/*`, `POST /multi-agent/*` |
| **Week 2 (Lec 42: Day 1)** | **LangChain vs LiteLLM: Choosing the Right Framework** | ✅ **Completed** | `week2/day1_langchain_vs_litellm.py` | `POST /frameworks/*` |
| **Week 2 (Day 2)** | Gradio UI Framework & Interactive Frontends | 🟡 **Next Up** | `week2/day2_gradio.py` | Port `7860` (Gradio) |
| **Week 2 (Day 3)** | Conversational AI & Memory Chatbots | ⚪ *Queued* | `week2/day3_chatbot.py` | `POST /conversation/*` |
| **Week 2 (Day 4 & 5)** | Capstone Airline AI Customer Support Assistant | ⚪ *Queued* | `week2/day4_airline_assistant.py` | SQLite + Gradio UI |
| **Weeks 3 – 8** | RAG, Vector Stores, Fine-Tuning, Agents & Deployment | ⚪ *Queued* | Weeks 3 to 8 modules | ChromaDB, Modal, LangGraph |

---

## 🏛️ WEEK 1: Foundations of LLMs & Web Intelligence

### Lecture Track Record (Week 1)

| Lecture / Section | Day | Topic | Practiced File | Testing Method | Status |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Lec 1 – 5** | Day 1 | Connecting to Frontier Models & Simple Ask | [`week1/day1_intro.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week1/day1_intro.py) | `python week1/day1_intro.py`<br>`POST /ask` | ✅ Completed |
| **Lec 6 – 10** | Day 2 | Prompt Engineering & System Roles (Pirate persona) | [`week1/day2_prompting.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week1/day2_prompting.py) | `python week1/day2_prompting.py`<br>`POST /ask` | ✅ Completed |
| **Lec 11 – 15** | Day 3 & 4 | Web Scraping & Single-Page Summarizer | [`week1/scraper.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week1/scraper.py)<br>[`week1/day4_summarizer.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week1/day4_summarizer.py) | `python week1/day4_summarizer.py`<br>`POST /website/summarize` | ✅ Completed |
| **Lec 16 – 20** | Day 5 | Multi-Page Web Brochure Generator (Capstone) | [`week1/day5_brochure.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week1/day5_brochure.py) | `python week1/day5_brochure.py`<br>`POST /website/brochure` | ✅ Completed |
| **Lec 21 – 25** | Bonus | Multi-Turn Stateful Memory Conversation | [`src/services/conversation.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/src/services/conversation.py) | `POST /conversation/` | ✅ Completed |

---

## 🚀 WEEK 2: Frontier APIs, Local Models, Frameworks & Multi-Agent Architecture

### Lecture Track Record (Week 2)

| Lecture / Section | Day | Topic | Practiced File | Testing Method | Status |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Lec 26 – 30** | Day 1 | Local Models with Ollama (`llama3.2`, `phi3`) & Provider Discovery | [`week2/day1/practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/practice.py) | `GET /models/providers`<br>`POST /models/query` | ✅ Completed |
| **Lec 31 – 35** | Day 1 | Reasoning Models & Inference-Time Scaling (`gpt-5-nano`) | [`week2/day1/practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/practice.py) | `POST /models/query`<br>*(Pushkin Bookworm & Probability Puzzles)* | ✅ Completed |
| **Lec 36 – 38** | Day 1 | Real-Time Token Streaming & Multi-Model Latency Benchmarking | [`week2/day1/practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/practice.py) | `POST /models/stream`<br>`POST /models/benchmark` | ✅ Completed |
| **Lec 39 – 41** | Day 1 | Autonomous Multi-Agent Conversations (2-Agent Debate & 3-Way Panel) | [`week2/day1/practice.py`](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1/practice.py) | `POST /multi-agent/debate`<br>`POST /multi-agent/three-way` | ✅ Completed |
| **Lec 42** | **Day 1** | **LangChain vs LiteLLM: Choosing the Right LLM Framework** | [**`week2/day1_langchain_vs_litellm.py`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day1_langchain_vs_litellm.py)<br>[**`week2/check_hamlet_gemini.py`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/check_hamlet_gemini.py)<br>[**`week2/demo_prompt_caching.py`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/demo_prompt_caching.py)<br>[**`POWERSHELL_RUN_GUIDE.txt`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/POWERSHELL_RUN_GUIDE.txt) | `python week2/day1_langchain_vs_litellm.py`<br>`python week2/demo_prompt_caching.py`<br>`POST /frameworks/compare` | ✅ **Completed** |
| **Lec 43 – 47** | Day 2 | Building User Interfaces with Gradio (Simple Chat, Custom Themes) | *Upcoming* | `gradio app.py` (Port 7860) | 🟡 Next Up |
| **Lec 48 – 52** | Day 3 | Conversational AI Assistants & Session Chat History | *Upcoming* | Gradio + FastAPI | ⚪ Queued |
| **Lec 53 – 60** | Day 4 & 5 | Airline AI Customer Support Assistant (SQLite + Tools) | *Upcoming* | Full Airline Project | ⚪ Queued |

---

## 🎯 Detailed Focus: Lec 42: Day 1 (LangChain vs LiteLLM)

### Key Architectural Takeaways:
1. **LiteLLM**:
   - Universal gateway for 100+ model providers following the standard OpenAI `completion()` syntax.
   - Ideal when your priority is avoiding vendor lock-in, tracking API spend (`completion_cost`), and routing between cloud & local models without bloated abstractions.
2. **LangChain**:
   - Comprehensive orchestration framework powered by LangChain Expression Language (LCEL: `prompt | model | parser`).
   - Ideal when your priority is multi-step sequential reasoning chains, Retrieval-Augmented Generation (RAG) with vector databases, and autonomous agents with tools.
3. **The Industry Hybrid Pattern**:
   - Build your workflow, prompts, and retrieval logic with **LangChain**, and route the underlying LLM calls through **LiteLLM** for universal provider access, retries, and spend monitoring.

---

## ⚡ Complete Testing Command Cheatsheet

### 1. Standalone Script Runners (Command Line)
```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

# Week 1 Capstone (Website Brochure Generator)
python week1/day5_brochure.py

# Week 2 Day 1 (Frontier Models, Reasoning, Ollama & Multi-Agent)
python week2/day1/practice.py

# Week 2 Lec 42: Day 1 (LangChain vs LiteLLM Comparison Suite)
python week2/day1_langchain_vs_litellm.py
```

### 2. FastAPI Server & Swagger UI
```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Key Endpoints Summary:
- `POST /ask` $\to$ Basic Frontier Model Ask
- `POST /website/summarize` $\to$ Single-page Web Summarizer
- `POST /website/brochure` $\to$ Multi-page Web Scraper & Brochure Generator
- `POST /conversation/` $\to$ Stateful Multi-Turn Chat
- `GET  /models/providers` $\to$ Local Ollama & Cloud Discovery
- `POST /models/query` $\to$ Unified Model Query (OpenAI, Ollama, Groq, Reasoning)
- `POST /models/stream` $\to$ Real-Time Token Streaming
- `POST /models/benchmark` $\to$ Model Latency & Token Benchmarking
- `POST /multi-agent/debate` $\to$ 2-Agent Adversarial Debate
- `POST /multi-agent/three-way` $\to$ 3-Way Panel Dialogue
- `POST /frameworks/litellm` $\to$ **[Lec 42]** LiteLLM Universal Gateway
- `POST /frameworks/langchain` $\to$ **[Lec 42]** LangChain LCEL Declarative Pipeline
- `POST /frameworks/compare` $\to$ **[Lec 42]** Side-by-Side Head-to-Head Benchmark
