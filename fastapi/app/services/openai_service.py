import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-5.6-luna"


def ask_openai(conversation):

    response = client.responses.create(
        model=MODEL,
        input=conversation
    )

    return response.output_text