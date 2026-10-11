"""
Week 1 Day 1 — First LLM API Call (OpenAI + Local Ollama)
=========================================================
Learn to connect to Frontier LLM APIs and local open-source models
using the universal OpenAI Python SDK.
"""

import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Safe UTF-8 output on Windows consoles
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

def run_day1_practice():
    print("=" * 60)
    print("🚀 Week 1 Day 1: First LLM API Calls")
    print("=" * 60)

    # 1. Test Cloud OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("\n1️⃣  Testing OpenAI (gpt-4o-mini)...")
        try:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": "Tell a 1-sentence joke for someone learning AI Engineering."}
                ]
            )
            print("   ✅ OpenAI Response:")
            print(f"   \"{response.choices[0].message.content.strip()}\"")
            print(f"   (Tokens used: {response.usage.total_tokens})")
        except Exception as e:
            print(f"   ❌ OpenAI call failed: {e}")
    else:
        print("\n1️⃣  OPENAI_API_KEY not found in .env (Skipping cloud call)")

    # 2. Test Local Ollama (Free, runs offline on your machine)
    print("\n2️⃣  Testing Local Ollama (llama3.2)...")
    try:
        ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = ollama_client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "user", "content": "What is an LLM in one sentence?"}
            ]
        )
        print("   ✅ Local Ollama Response:")
        print(f"   \"{response.choices[0].message.content.strip()}\"")
    except Exception as e:
        print(f"   ⚠️  Ollama connection failed: {e}")
        print("   Make sure Ollama is running in background (run 'ollama serve' if needed).")

    print("\n" + "=" * 60)
    print("🎉 Week 1 Day 1 completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_day1_practice()
