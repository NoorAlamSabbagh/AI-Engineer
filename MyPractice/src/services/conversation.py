import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_chat_response(new_message: str, history: list, system_prompt: str) -> dict:
    """Builds the complete message chain and queries OpenAI."""
    # 1. Start with the system prompt
    formatted_messages = [
        {"role": "system", "content": system_prompt}
    ]

    # 2. Append past conversation turns
    for turn in history:
        # Handles both dict and Pydantic object
        role = turn.role if hasattr(turn, "role") else turn.get("role")
        content = turn.content if hasattr(turn, "content") else turn.get("content")
        formatted_messages.append({"role": role, "content": content})

    # 3. Append the newest user message
    formatted_messages.append({"role": "user", "content": new_message})

    # 4. Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=formatted_messages
    )

    ai_reply = response.choices[0].message.content

    # 5. Return updated history including this new exchange
    updated_history = [
        {"role": turn.role if hasattr(turn, "role") else turn["role"], 
         "content": turn.content if hasattr(turn, "content") else turn["content"]}
        for turn in history
    ]
    updated_history.append({"role": "user", "content": new_message})
    updated_history.append({"role": "assistant", "content": ai_reply})

    return {
        "reply": ai_reply,
        "updated_history": updated_history
    }
