import os
from dotenv import load_dotenv

# 1. Load environment variables first before importing modules that need them
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from src.routes.website import router as website_router
from src.routes.conversation import router as conversation_router
from src.routes.models import router as models_router
from src.routes.multi_agent import router as multi_agent_router
# [Lec 42: Day 1] Import LangChain vs LiteLLM frameworks router
from src.routes.frameworks import router as frameworks_router
# [Lec 44–48: Day 2] Import Gradio UI router & service for Swagger Docs & Web UI
import gradio as gr
from src.routes.gradio_ui import router as gradio_router
from src.services.gradio_service import create_gradio_app

# 2. Initialize FastAPI app
app = FastAPI(
    title="AI Engineering Practice API",
    description="Hands-on practice API implementing clean 4-layer architecture for Frontier Model APIs, Local Ollama, Streaming, Multi-Agent Systems, LangChain, LiteLLM, and Gradio Web UIs (Lec 44–48).",
    version="2.2.0"
)

# 3. Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 4. Define the Request Schema (Data shape expected from Postman)
class PromptRequest(BaseModel):
    prompt: str

# Register application routers
app.include_router(website_router)
app.include_router(conversation_router)
app.include_router(models_router)
app.include_router(multi_agent_router)
# [Lec 42: Day 1] Register LangChain vs LiteLLM frameworks endpoints
app.include_router(frameworks_router)
# [Lec 44–48: Day 2] Register Gradio UI endpoints
app.include_router(gradio_router)

# Mount interactive Gradio UI directly onto FastAPI at /gradio
gradio_interface = create_gradio_app()
app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")

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
