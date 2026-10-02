import os
from dotenv import load_dotenv

# 1. Load environment variables first before importing modules that need them
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from src.routes.website import router as website_router
from src.routes.conversation import router as conversation_router

# 2. Initialize FastAPI app
app = FastAPI(
    title="AI Engineering Practice API",
    version="1.0.0"
)

# 3. Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 4. Define the Request Schema (Data shape expected from Postman)
class PromptRequest(BaseModel):
    prompt: str

# Register the website router
app.include_router(website_router)
app.include_router(conversation_router)

# 5. Existing Health Check (GET)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Engineering API is running smoothly!"
    }


# 6. New AI Endpoint (POST)
@app.post("/ask")
def ask_ai(request: PromptRequest):
    try:
        # Send prompt to OpenAI model (gpt-4o-mini is fast, reliable, and cost-effective)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, expert AI Engineering assistant."
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
        )

        ai_message = response.choices[0].message.content

        return {
            "status": "success",
            "prompt": request.prompt,
            "response": ai_message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
