from app.services.openai_service import ask_openai as ask_suresh
from app.services.huggingface import ask_huggingface as ask_ramesh


def start_conversation(first_message, rounds=5):

    conversation = [
        {
            "speaker": "User",
            "message": first_message
        }
    ]

    for round_number in range(rounds):

        # =========================
        # SURESH - OpenAI
        # =========================

        suresh_prompt = []

        suresh_prompt.append({
            "role": "developer",
            "content": """
You are Suresh.

You are having a natural conversation with Ramesh.

Ramesh is another AI model.

Remember everything that has been said previously.

Do not mention that you are an AI unless the conversation requires it.

Respond naturally like a human named Suresh.
"""
        })

        for message in conversation:

            suresh_prompt.append({
                "role": "user",
                "content": f"{message['speaker']}: {message['message']}"
            })

        suresh_response = ask_suresh(suresh_prompt)

        print(f"\nSuresh: {suresh_response}")

        conversation.append({
            "speaker": "Suresh",
            "message": suresh_response
        })


        # =========================
        # RAMESH - Hugging Face
        # =========================

        ramesh_prompt = []

        ramesh_prompt.append({
            "role": "system",
            "content": """
You are Ramesh.

You are having a natural conversation with Suresh.

Suresh is another AI model.

Remember everything that has been said previously.

Do not mention that you are an AI unless the conversation requires it.

Respond naturally like a human named Ramesh.
"""
        })

        for message in conversation:

            ramesh_prompt.append({
                "role": "user",
                "content": f"{message['speaker']}: {message['message']}"
            })

        ramesh_response = ask_ramesh(ramesh_prompt)

        print(f"\nRamesh: {ramesh_response}")

        conversation.append({
            "speaker": "Ramesh",
            "message": ramesh_response
        })


    return conversation