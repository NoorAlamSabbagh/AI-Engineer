from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str       # "user" or "assistant"
    content: str

class ChatConversationRequest(BaseModel):
    message: str                             # The new message from the user
    history: Optional[List[ChatMessage]] = [] # Previous chat messages
    system_prompt: Optional[str] = "You are a knowledgeable AI tutor helping students learn AI Engineering."
