from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from app.routes.user import router as user_router
from app.routes.website import router as website_router
from app.routes.conversation import router as conversation_router

load_dotenv()

app=FastAPI()

client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class PromptRequest(BaseModel):
    prompt:str


app.include_router(user_router)
app.include_router(website_router)
app.include_router(conversation_router)


@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/ask")
def ask_ai(request:PromptRequest):
    response=client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You are a helpful assistant for a background verification company."
            },
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    )

    return {
        "response":response.output_text
    }

