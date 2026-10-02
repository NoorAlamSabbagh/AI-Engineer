from fastapi import APIRouter
from src.schemas.conversation import ChatConversationRequest
from src.controllers.conversation import chat_controller

router = APIRouter(
    prefix="/conversation",
    tags=["Chat & Conversation"]
)

@router.post("/")
def chat_endpoint(request: ChatConversationRequest):
    return chat_controller(request)
