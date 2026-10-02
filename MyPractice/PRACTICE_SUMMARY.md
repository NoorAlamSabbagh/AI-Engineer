# AI Engineering Practice — Fast Track Guide & Progress Summary

This document records everything completed during our session, how to restart your server tomorrow, and test payloads for Postman.

---

## 🚀 How to Resume Work Tomorrow

When you open your terminal tomorrow in VS Code / IDE:

```powershell
# 1. Navigate to your practice directory
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Start the FastAPI development server
uvicorn src.main:app --reload
```

Your API will be running at: `http://127.0.0.1:8000`  
Interactive Swagger Documentation: `http://127.0.0.1:8000/docs`

---

## 📁 Architecture Overview

Your project follows the 4-layer clean architecture:

```
MyPractice/
├── .env                  # Secret keys (OPENAI_API_KEY, HUGGINGFACE_API_KEY) - never committed
├── .env.example          # Public template for environment variables
├── requirements.txt      # Dependencies (fastapi, uvicorn, openai, bs4, requests, etc.)
└── src/
    ├── main.py           # App initialization, middleware, router inclusions
    ├── routes/           # URL declarations (APIRouter)
    │   ├── website.py
    │   └── conversation.py
    ├── controllers/      # Request flow orchestration and error handling
    │   ├── website.py
    │   └── conversation.py
    ├── services/         # Heavy lifting (OpenAI calls, Web Scraping)
    │   ├── website.py
    │   └── conversation.py
    └── schemas/          # Pydantic models for JSON validation
        ├── website.py
        └── conversation.py
```

---

## 📬 Completed Postman Endpoints & Test Payloads

### 1. Health Check
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/health`
- **Response**: `{"status": "ok", "message": "AI Engineering API is running smoothly!"}`

---

### 2. Basic Prompt Endpoint
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/ask`
- **Headers**: `Content-Type: application/json`
- **Body (raw JSON)**:
```json
{
  "prompt": "What is an LLM in two sentences?"
}
```

---

### 3. Single-Page Website Summarizer
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/website/summarize`
- **Headers**: `Content-Type: application/json`
- **Body (raw JSON)**:
```json
{
  "url": "https://example.com",
  "tone": "enthusiastic and modern"
}
```

---

### 4. Week 1 Capstone: Multi-Page Brochure Generator
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/website/brochure`
- **Headers**: `Content-Type: application/json`
- **Body (raw JSON)**:
```json
{
  "company_name": "Edward Donner",
  "url": "https://edwarddonner.com"
}
```

---

### 5. Multi-Turn Conversation API with Memory
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/conversation/`
- **Headers**: `Content-Type: application/json`

**Turn 1 Body (Starting the chat):**
```json
{
  "message": "Hi, my name is Alam and I am learning AI Engineering!"
}
```

**Turn 2 Body (Follow-up with history passed back):**
```json
{
  "message": "What is my name and what am I studying?",
  "history": [
    {
      "role": "user",
      "content": "Hi, my name is Alam and I am learning AI Engineering!"
    },
    {
      "role": "assistant",
      "content": "Hello Alam! Great to meet you..."
    }
  ]
}
```

---

## 🎯 Next Topics for Tomorrow
1. **Real-time Token Streaming (`StreamingResponse`)**: Stream text token by token rather than waiting for completion.
2. **Hugging Face Open-Source Model Integration**: Connect your `HUGGINGFACE_API_KEY` to run alternative models.
3. **Autonomous AI-to-AI Mock Interview (`POST /conversation/interview`)**: Two AI personas (Interviewer & Candidate) holding an automated technical interview.
