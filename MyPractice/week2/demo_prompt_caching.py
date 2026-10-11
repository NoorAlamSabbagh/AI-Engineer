# ==============================================================================
# Lec 42: Day 1 — LiteLLM Pro-Feature: Prompt Caching
# File: MyPractice/week2/demo_prompt_caching.py
# ==============================================================================
# Step-by-step implementation of Cell 59 to Cell 67 from week2/day1.ipynb:
# Demonstrates how LiteLLM interfaces with provider prompt caching (OpenAI/Gemini)
# to drastically reduce input token costs for large documents (e.g. Shakespeare's Hamlet).
# ==============================================================================

import os
import sys
import io
import time
from dotenv import load_dotenv
import litellm
from litellm import completion, completion_cost

# Ensure UTF-8 output on Windows console
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# [Lec 42: Day 1] Load environment variables
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

HAMLET_PATH = os.path.join(CURRENT_DIR, "hamlet.txt")


def lec42_day1_prompt_caching_demo():
    """
    [Lec 42: Day 1] Step-by-Step Prompt Caching Walkthrough:
    - Step 1: Read the large text document (Hamlet text, ~40k tokens).
    - Step 2: Formulate baseline user query (short prompt without context).
    - Step 3: Run baseline call and inspect tokens & cost.
    - Step 4: Inject the massive context (hamlet) into the prompt string.
    - Step 5: Cold Call (First large request) -> Populates/primes the model's cache.
    - Step 6: Warm Call (Second request with identical prefix) -> Triggers Cache Hit!
    - Step 7: Inspect cached_tokens and compare cost savings.
    """
    print("=" * 75)
    print("🎭 [Lec 42: Day 1] PRO-FEATURE: PROMPT CACHING WITH LITELLM")
    print("=" * 75)

    # --------------------------------------------------------------------------
    # Step 1: Load the Large Document String (hamlet.txt)
    # --------------------------------------------------------------------------
    print("\n📂 [Step 1] Loading Hamlet text file...")
    if not os.path.exists(HAMLET_PATH):
        raise FileNotFoundError(f"Cannot find hamlet.txt at {HAMLET_PATH}")

    with open(HAMLET_PATH, "r", encoding="utf-8") as f:
        hamlet_text = f.read()

    loc = hamlet_text.find("Speak, man")
    snippet = hamlet_text[loc : loc + 100].replace("\n", " ")
    print(f"   • Loaded text size: {len(hamlet_text):,} characters (~{len(hamlet_text)//4:,} tokens)")
    print(f"   • Text snippet: \"{snippet}...\"")

    # --------------------------------------------------------------------------
    # Step 2: Prepare the Baseline Query (Small Prompt)
    # --------------------------------------------------------------------------
    # Which string is passed where:
    # 'question_str': The exact question to ask the LLM.
    # 'messages': List of dicts passed to completion(messages=...)
    # --------------------------------------------------------------------------
    question_str = "In Hamlet, when Laertes asks 'Where is my father?' what is the reply?"
    messages_baseline = [{"role": "user", "content": question_str}]

    # Select model: Use gpt-4o-mini (OpenAI has automatic prompt caching for >=1024 tokens)
    # or gemini/gemini-2.0-flash / gemini-1.5-flash
    model_name = "gpt-4o-mini"
    print(f"\n🤖 [Step 2] Using Model: {model_name}")

    # --------------------------------------------------------------------------
    # Step 3: Baseline Call (Without the massive context)
    # --------------------------------------------------------------------------
    print("\n▶️  [Step 3] Baseline Call (Short prompt, no document attached)...")
    resp_baseline = completion(model=model_name, messages=messages_baseline)
    reply_baseline = resp_baseline.choices[0].message.content.strip()
    print(f"   Answer: {reply_baseline[:120]}...\n")

    # Inspect tokens and cost
    prompt_tok = resp_baseline.usage.prompt_tokens
    comp_tok = resp_baseline.usage.completion_tokens
    tot_tok = resp_baseline.usage.total_tokens
    cost_baseline = getattr(resp_baseline, "_hidden_params", {}).get("response_cost")
    if cost_baseline is None:
        cost_baseline = completion_cost(completion_response=resp_baseline)

    print(f"   Input tokens:  {prompt_tok}")
    print(f"   Output tokens: {comp_tok}")
    print(f"   Total tokens:  {tot_tok}")
    print(f"   Total cost:    {cost_baseline * 100:.4f} cents (${cost_baseline:.6f} USD)")

    # --------------------------------------------------------------------------
    # Step 4: Construct the Cached Prompt (String placement rule)
    # --------------------------------------------------------------------------
    # CRITICAL RULE FOR PROMPT CACHING:
    # Providers (OpenAI & Anthropic) cache by PREFIX MATCH.
    # The large static text MUST appear at the beginning or as the system message,
    # and stay identical across repeated calls!
    # --------------------------------------------------------------------------
    print("\n📦 [Step 4] Assembling Prompt with Full Hamlet Context (~40k tokens)...")
    # In Ed Donner's lecture (Cell 63):
    # question[0]["content"] += "\n\nFor context, here is the entire text of Hamlet:\n\n" + hamlet
    # To maximize OpenAI / Anthropic prefix caching, we place the static context first:
    cached_messages = [
        {
            "role": "system",
            "content": f"You are a Shakespeare scholar. Use the following full text of Hamlet as your reference:\n\n{hamlet_text}",
        },
        {
            "role": "user",
            "content": question_str,
        },
    ]
    print(f"   • Total message length: {len(cached_messages[0]['content']) + len(cached_messages[1]['content']):,} characters")

    # --------------------------------------------------------------------------
    # Step 5: Cold Call (First Request with Large Context)
    # --------------------------------------------------------------------------
    # The model processes all ~40k tokens from scratch and writes them to the cache.
    # --------------------------------------------------------------------------
    print("\n❄️  [Step 5] Call 1 (Cold Cache) — Processing full text & priming cache...")
    start_t1 = time.time()
    resp_call1 = completion(model=model_name, messages=cached_messages)
    elapsed_t1 = time.time() - start_t1

    prompt_tok_1 = resp_call1.usage.prompt_tokens
    comp_tok_1 = resp_call1.usage.completion_tokens
    # Check cached tokens in prompt_tokens_details
    details_1 = getattr(resp_call1.usage, "prompt_tokens_details", None)
    cached_tok_1 = getattr(details_1, "cached_tokens", 0) if details_1 else 0
    cost_1 = getattr(resp_call1, "_hidden_params", {}).get("response_cost")
    if cost_1 is None:
        cost_1 = completion_cost(completion_response=resp_call1)

    print(f"   Response time: {elapsed_t1:.2f}s")
    print(f"   Answer:        {resp_call1.choices[0].message.content.strip()[:100]}...")
    print(f"   Input tokens:  {prompt_tok_1}")
    print(f"   Output tokens: {comp_tok_1}")
    print(f"   Cached tokens: {cached_tok_1} (Cold run: cache not populated yet)")
    print(f"   Total cost:    {cost_1 * 100:.4f} cents (${cost_1:.6f} USD)")

    # --------------------------------------------------------------------------
    # Step 6: Warm Call (Second Request with Same Context Prefix)
    # --------------------------------------------------------------------------
    # We ask a second question using the exact same static system text.
    # Because the prefix matches, the model reads the 40k tokens from cache!
    # --------------------------------------------------------------------------
    print("\n🔥 [Step 6] Call 2 (Warm Cache) — Same context prefix, new user query...")
    cached_messages_call2 = [
        cached_messages[0],  # Exact same static Shakespeare context prefix
        {"role": "user", "content": "What are Hamlet's famous first words in Act 1 Scene 2?"},
    ]

    start_t2 = time.time()
    resp_call2 = completion(model=model_name, messages=cached_messages_call2)
    elapsed_t2 = time.time() - start_t2

    prompt_tok_2 = resp_call2.usage.prompt_tokens
    comp_tok_2 = resp_call2.usage.completion_tokens
    details_2 = getattr(resp_call2.usage, "prompt_tokens_details", None)
    cached_tok_2 = getattr(details_2, "cached_tokens", 0) if details_2 else 0
    cost_2 = getattr(resp_call2, "_hidden_params", {}).get("response_cost")
    if cost_2 is None:
        cost_2 = completion_cost(completion_response=resp_call2)

    print(f"   Response time: {elapsed_t2:.2f}s (Faster latency!)")
    print(f"   Answer:        {resp_call2.choices[0].message.content.strip()[:100]}...")
    print(f"   Input tokens:  {prompt_tok_2}")
    print(f"   Output tokens: {comp_tok_2}")
    print(f"   Cached tokens: {cached_tok_2} (Cache hit! Reused from memory)")
    print(f"   Total cost:    {cost_2 * 100:.4f} cents (${cost_2:.6f} USD)")

    # --------------------------------------------------------------------------
    # Step 7: Summary of Findings & Where to Check
    # --------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("📊 [Lec 42: Day 1] SUMMARY: PROMPT CACHING METRICS")
    print("=" * 75)
    print(f"1. Input Tokens:    {prompt_tok_2} (Read from input)")
    print(f"2. Cached Tokens:   {cached_tok_2} (Discounted by provider)")
    if cost_1 > 0:
        savings = max(0.0, (1.0 - (cost_2 / cost_1)) * 100.0)
        print(f"3. Cost Reduction:  {savings:.1f}% cheaper on warm call!")
    print(f"4. Cost Metric:     {cost_2 * 100:.4f} cents")
    print("=" * 75)


if __name__ == "__main__":
    lec42_day1_prompt_caching_demo()
