import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

MODEL = "meta-llama/Llama-3.1-8B-Instruct"


def ask_huggingface(conversation):

    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        max_tokens=500
    )

    return response.choices[0].message.content