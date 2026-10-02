from fastapi import APIRouter

from app.controllers.conversation import (create_conversation,run_interview)
from app.schemas.conversation import ConversationRequest


router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"]
)


@router.post("/")
def conversation(request: ConversationRequest):

    return create_conversation(
        request.message
    )

@router.post("/interview")
def interview():

    return run_interview()