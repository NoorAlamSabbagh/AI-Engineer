from fastapi import HTTPException
from src.schemas.conversation import ChatConversationRequest
from src.services.conversation import generate_chat_response

def chat_controller(request: ChatConversationRequest):
    try:
        result = generate_chat_response(
            new_message=request.message,
            history=request.history,
            system_prompt=request.system_prompt
        )
        return {
            "status": "success",
            "reply": result["reply"],
            "conversation_history": result["updated_history"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
