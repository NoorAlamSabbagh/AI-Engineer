from pydantic import BaseModel


class ConversationRequest(BaseModel):
    message: str