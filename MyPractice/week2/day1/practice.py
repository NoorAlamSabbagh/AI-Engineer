"""
Week 2 Day 1 — Frontier APIs, Local Models & Multi-Agent Dialogue
================================================================
Covers:
1. Connecting to Local Ollama & Cloud OpenAI using the OpenAI Universal Client
2. Real-time streaming
3. Autonomous 2-Agent Adversarial Debate
4. 3-Way Multi-Agent Round Robin Dialogue
"""

import os
import io
import sys
from dotenv import load_dotenv

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from openai import OpenAI

# We import the tested services from src/services
from src.services.model_provider import call_llm, get_provider_status
from src.services.multi_agent import run_two_agent_debate, run_three_way_round_robin

def run_week2_day1():
    print("=" * 65)
    print("🚀 WEEK 2 DAY 1: Frontier APIs, Local Models & Multi-Agent Conversations")
    print("=" * 65)

    # 1. Discover local & cloud models
    print("\n1️⃣  Active Providers & Models:")
    status = get_provider_status()
    for prov, data in status.items():
        state = "ONLINE" if data.get("available") else "OFFLINE"
        print(f"   • {prov.upper():<8} [{data.get('type')}]: {state}")
        if prov == "ollama" and data.get("installed_models"):
            print(f"     └─ Local models found: {', '.join(data['installed_models'])}")

    # 2. Local vs Cloud prompt test
    print("\n2️⃣  Comparing Local Ollama (llama3.2) vs Cloud OpenAI (gpt-4o-mini):")
    prompt = [{"role": "user", "content": "What is prompt caching in 2 sentences?"}]
    
    print("   [Ollama llama3.2]:")
    res_local = call_llm(provider="ollama", model="llama3.2", messages=prompt)
    print(f"   \"{res_local['content'].strip()}\" ({res_local['duration_seconds']}s)\n")

    print("   [OpenAI gpt-4o-mini]:")
    res_cloud = call_llm(provider="openai", model="gpt-4o-mini", messages=prompt)
    print(f"   \"{res_cloud['content'].strip()}\" ({res_cloud['duration_seconds']}s)\n")

    # 3. Training vs Inference-Time Scaling (Reasoning Puzzle)
    print("\n3️⃣  Inference-Time Scaling (Reasoning Puzzle with gpt-5-nano):")
    easy_puzzle = [
        {"role": "user", "content": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."}
    ]
    print("   Puzzle: \"You toss 2 coins. One of them is heads. What's the probability the other is tails?\"")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # minimal reasoning effort (fast, intuitive answer)
    res_minimal = client.chat.completions.create(
        model="gpt-5-nano",
        messages=easy_puzzle,
        reasoning_effort="minimal"
    )
    ans_minimal = res_minimal.choices[0].message.content.strip()
    print(f"   • reasoning_effort='minimal': {ans_minimal} (Fast intuitive answer)")

    # low reasoning effort (thinks through conditional probability)
    res_low = client.chat.completions.create(
        model="gpt-5-nano",
        messages=easy_puzzle,
        reasoning_effort="low"
    )
    ans_low = res_low.choices[0].message.content.strip()
    print(f"   • reasoning_effort='low':     {ans_low} (Correct conditional probability)\n")

    # Hard Puzzle: Testing Frontier Reasoning (Pushkin Bookworm Puzzle)
    print("   🧠 [Hard Puzzle: Testing Frontier Models on the Planet]:")
    hard = """On a bookshelf, two volumes of Pushkin stand side by side: the first and the second.
The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick.
A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume.
What distance did it gnaw through?"""
    hard_puzzle = [{"role": "user", "content": hard}]

    print("   Testing gpt-5-nano (reasoning_effort='minimal'):")
    res_hard_nano = client.chat.completions.create(
        model="gpt-5-nano",
        messages=hard_puzzle,
        reasoning_effort="minimal"
    )
    print(f"   \"\"\"{res_hard_nano.choices[0].message.content.strip()}\"\"\"\n")

    print("   Testing frontier gpt-5:")
    try:
        res_hard_gpt5 = client.chat.completions.create(
            model="gpt-5",
            messages=hard_puzzle
        )
        print(f"   \"\"\"{res_hard_gpt5.choices[0].message.content.strip()}\"\"\"\n")
    except Exception as e:
        print(f"   (gpt-5 unavailable: {e})\n")

    # A spicy challenge to test the competitive spirit (Game Theory Prisoner's Dilemma)
    print("   🌶️ [A spicy challenge to test the competitive spirit]:")
    dilemma_prompt = """You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:
Cooperate: Choose "Share" — if both of you choose this, you each win $1,000.
Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.
If both steal, you both get nothing.
Do you choose to Steal or Share? Pick one."""

    dilemma = [
        {"role": "user", "content": dilemma_prompt},
    ]

    print("   Testing gpt-4o-mini:")
    res_dilemma_mini = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=dilemma
    )
    print(f"   [gpt-4o-mini]: \"{res_dilemma_mini.choices[0].message.content.strip()}\"\n")

    print("   Testing reasoning model gpt-5-nano:")
    res_dilemma_nano = client.chat.completions.create(
        model="gpt-5-nano",
        messages=dilemma,
        reasoning_effort="low"
    )
    print(f"   [gpt-5-nano]: \"{res_dilemma_nano.choices[0].message.content.strip()}\"\n")

    # 4. 2-Agent Debate
    print("\n4️⃣  Autonomous 2-Agent Debate (Alex vs Blake):")
    debate = run_two_agent_debate(
        topic="Will open-source local models make proprietary cloud models obsolete?",
        rounds=2
    )
    for turn in debate["transcript"]:
        print(f"\n   [{turn['speaker']}]:")
        print(f"   \"{turn['message'].strip()}\"")

    # 5. 3-Way Conversation
    print("\n\n5️⃣  3-Way Round Robin Conversation (Alex, Blake, Pierre):")
    three_way = run_three_way_round_robin(
        topic="How will AI change the day-to-day work of software engineers?",
        rounds=1
    )
    for turn in three_way["transcript"]:
        print(f"\n   [{turn['speaker']}]:")
        print(f"   \"{turn['message'].strip()}\"")

    # ==============================================================================
    # 6. [Lec 42: Day 1] LangChain vs LiteLLM: Choosing the Right LLM Framework
    # ==============================================================================
    print("\n\n6️⃣  [Lec 42: Day 1] LangChain vs LiteLLM Side-by-Side Comparison:")
    from src.services.framework_comparison import compare_frameworks
    comp = compare_frameworks(
        prompt="Explain vector databases in one concise sentence.",
        model_name="gpt-4o-mini"
    )
    print(f"   • LiteLLM   ({comp['litellm_result']['latency_seconds']}s): {comp['litellm_result']['response'].strip()}")
    print(f"   • LangChain ({comp['langchain_result']['latency_seconds']}s): {comp['langchain_result']['response'].strip()}")
    print(f"   • Lecture Recommendation: {comp['recommendation']['hybrid_pattern']}")

    print("\n" + "=" * 65)
    print("🎉 Week 2 Day 1 Practice Completed!")
    print("=" * 65)

if __name__ == "__main__":
    run_week2_day1()
