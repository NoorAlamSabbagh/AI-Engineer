"""
Week 1 Final Exercise Solution
==============================
Builds a technical explanation assistant demonstrating:
1. Streaming explanation using OpenAI (gpt-4o-mini).
2. Offline explanation using Local Ollama (llama3.2).
"""

import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"

QUESTION = """
Please explain what this Python code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""

def explain_with_openai_streaming(question: str):
    print("=" * 60)
    print("1️⃣  Answering via OpenAI (gpt-4o-mini) with Live Streaming:")
    print("=" * 60)
    
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("⚠️ OPENAI_API_KEY is not set.")
        return

    client = OpenAI(api_key=key)
    stream = client.chat.completions.create(
        model=MODEL_GPT,
        messages=[
            {"role": "system", "content": "You are an expert Python engineering mentor. Explain code clearly with concise breakdown."},
            {"role": "user", "content": question}
        ],
        stream=True
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")

def explain_with_ollama(question: str):
    print("=" * 60)
    print("2️⃣  Answering via Local Ollama (llama3.2) - Offline & Free:")
    print("=" * 60)
    
    try:
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = client.chat.completions.create(
            model=MODEL_LLAMA,
            messages=[
                {"role": "system", "content": "You are a helpful Python expert."},
                {"role": "user", "content": question}
            ]
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
    print("\n")

if __name__ == "__main__":
    print(f"Question:\n{QUESTION.strip()}\n")
    explain_with_openai_streaming(QUESTION)
    explain_with_ollama(QUESTION)
    print("🎉 Week 1 Exercise completed successfully!")
