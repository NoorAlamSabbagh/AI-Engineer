"""
Week 1 Day 2 — Prompt Engineering, Personas & Parameters
========================================================
Learn how system prompts, personas, few-shot examples,
and temperature influence the model's behavior.
Works with either OpenAI or Local Ollama.
"""

import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

def get_client_and_model():
    """Returns OpenAI client if key is set, otherwise falls back to local Ollama."""
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return OpenAI(api_key=key), "gpt-4o-mini", "OpenAI (Cloud)"
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "llama3.2", "Ollama (Local)"

def run_day2_practice():
    client, model_name, provider_label = get_client_and_model()
    print("=" * 60)
    print(f"🚀 Week 1 Day 2: Prompt Engineering using {provider_label}")
    print("=" * 60)

    # 1. System Prompt & Persona Comparison
    print("\n1️⃣  Testing Personas:")
    prompt = "Explain quantum computing in 2 sentences."
    
    personas = [
        ("ELI5 Persona", "You are a kindergarten teacher who explains advanced concepts using simple everyday toys."),
        ("Snarky Pirate", "You are a witty, sarcastic pirate captain who uses pirate slang and metaphors.")
    ]

    for label, system_prompt in personas:
        print(f"\n   🎭 Persona: {label}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        res = client.chat.completions.create(model=model_name, messages=messages)
        print(f"   💬 Output:\n   {res.choices[0].message.content.strip()}\n")

    # 2. Few-Shot Prompting (Teaching by Example)
    print("\n2️⃣  Few-Shot Prompting (Custom sentiment & emoji classification):")
    few_shot_messages = [
        {"role": "system", "content": "Classify sentiment and output only: <SENTIMENT> | <EMOJI>."},
        {"role": "user", "content": "I just passed my AI exam!"},
        {"role": "assistant", "content": "POSITIVE | 🎓🎉"},
        {"role": "user", "content": "My server crashed in production at 3 AM."},
        {"role": "assistant", "content": "NEGATIVE | 💥🚨"},
        {"role": "user", "content": "Today we had pizza for lunch."}
    ]
    res = client.chat.completions.create(model=model_name, messages=few_shot_messages)
    print(f"   Input: 'Today we had pizza for lunch.'")
    print(f"   Output: {res.choices[0].message.content.strip()}")

    # 3. Temperature Parameter Control (Creative vs Deterministic)
    print("\n3️⃣  Temperature Comparison (Deterministic vs Creative):")
    creative_prompt = [
        {"role": "user", "content": "Invent a 2-word startup name for an autonomous AI coffee robot."}
    ]
    
    print("   Deterministic (temperature=0.0):")
    res_cold = client.chat.completions.create(model=model_name, messages=creative_prompt, temperature=0.0)
    print(f"   -> {res_cold.choices[0].message.content.strip()}")

    print("   Creative (temperature=1.2):")
    res_hot = client.chat.completions.create(model=model_name, messages=creative_prompt, temperature=1.2)
    print(f"   -> {res_hot.choices[0].message.content.strip()}")

    print("\n" + "=" * 60)
    print("🎉 Week 1 Day 2 completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_day2_practice()
