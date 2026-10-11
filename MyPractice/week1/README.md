# 📁 Week 1 — Day-by-Day API Testing Guide

Comprehensive testing guide for all **Week 1** exercises. You can test each day either via the **FastAPI HTTP Endpoint (Postman / Swagger UI)** or via the **Standalone Python script**.

---

## ⚡ Prerequisites

Start your FastAPI server from the project root:
```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Standard Header for all POST requests**: `Content-Type: application/json`

---

## 📅 Day 1 — Connecting to OpenAI API & Universal Client

### Concept
Sending prompts to OpenAI (`gpt-4o-mini`) and receiving model completions.

### 🌐 How to test via API
- **Endpoint**: `POST http://127.0.0.1:8000/ask`
- **Headers**:
  ```http
  Content-Type: application/json
  ```
- **Request Body (raw JSON)**:
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

### 💻 How to test via Terminal
```powershell
python week1/day1_intro.py
```

---

## 📅 Day 2 — Prompt Engineering, Personas & System Roles

### Concept
Steering LLM behavior, tone, constraints, and personas using system prompts.

### 🌐 How to test via API
- **Endpoint**: `POST http://127.0.0.1:8000/ask`
- **Headers**:
  ```http
  Content-Type: application/json
  ```
- **Request Body (raw JSON)**:
  ```json
  {
    "prompt": "Explain quantum computing to a 7-year-old child using a pirate accent."
  }
  ```
- **Expected Response**:
  ```json
  {
    "status": "success",
    "reply": "Ahoy, young matey! Imagine ye have a magical pirate coin that can spin on the deck..."
  }
  ```

### 💻 How to test via Terminal
```powershell
python week1/day2_prompting.py
```

---

## 📅 Day 3 — Web Scraping & Content Sanitization

### Concept
Fetching live HTML via BeautifulSoup, filtering out scripts, styles, and navigational junk to extract clean text.

### 🌐 How to test via API (Clean Scraped Text Preview)
- **Endpoint**: `POST http://127.0.0.1:8000/website/summarize`
- **Headers**:
  ```http
  Content-Type: application/json
  ```
- **Request Body (raw JSON)**:
  ```json
  {
    "url": "https://example.com",
    "tone": "neutral"
  }
  ```

### 💻 How to test via Terminal
```powershell
python week1/scraper.py
```

---

## 📅 Day 4 — Live Web Summarizer with Configurable Tone

### Concept
Combines web scraping with an LLM prompt to summarize any real-world URL into customized tones (e.g., executive, enthusiastic, critical).

### 🌐 How to test via API
- **Endpoint**: `POST http://127.0.0.1:8000/website/summarize`
- **Headers**:
  ```http
  Content-Type: application/json
  ```
- **Request Body (raw JSON)**:
  ```json
  {
    "url": "https://example.com",
    "tone": "enthusiastic and modern"
  }
  ```
- **Expected Response**:
  ```json
  {
    "status": "success",
    "url": "https://example.com",
    "tone": "enthusiastic and modern",
    "summary": "Example Domain is an iconic website operated by IANA that serves as a dependable standard..."
  }
  ```

### 💻 How to test via Terminal
```powershell
python week1/day4_summarizer.py
```

---

## 📅 Day 5 — Multi-Page Web Brochure Generator (Capstone)

### Concept
Crawls a company website, discovers internal navigation links (e.g. About, Careers, Products), extracts text across pages, and synthesizes a full marketing brochure.

### 🌐 How to test via API
- **Endpoint**: `POST http://127.0.0.1:8000/website/brochure`
- **Headers**:
  ```http
  Content-Type: application/json
  ```
- **Request Body (raw JSON)**:
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

### 💻 How to test via Terminal
```powershell
python week1/day5_brochure.py
```

---

## 📅 Week 1 Bonus — Multi-Turn Stateful Conversation API

### Concept
Maintains conversational memory by accepting previous chat turns in the payload and answering with full context awareness.

### 🌐 How to test via API
- **Endpoint**: `POST http://127.0.0.1:8000/conversation/`
- **Headers**:
  ```http
  Content-Type: application/json
  ```

#### Turn 1: Introduce yourself
- **Request Body**:
  ```json
  {
    "message": "Hi, my name is Alam and I am building an AI Engineering backend."
  }
  ```

#### Turn 2: Ask follow-up question (Pass previous history back in body)
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
        "content": "Hello Alam! Great to meet you. You are building an AI Engineering backend."
      }
    ]
  }
  ```
- **Expected Response**: The assistant correctly answers using the passed context.

---

## 📅 Week 1 Final Challenge — Technical Q&A Assistant
- **Terminal Execution**:
  ```powershell
  python week1/exercise_solution.py
  ```
