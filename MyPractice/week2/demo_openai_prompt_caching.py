# ==============================================================================
# Lec 42: Day 1 — Dedicated Deep-Dive: OpenAI Prompt Caching
# File: MyPractice/week2/demo_openai_prompt_caching.py
# ==============================================================================
# Topic: Prompt Caching with OpenAI
# Reference: https://platform.openai.com/docs/guides/prompt-caching
# Pricing:   https://openai.com/api/pricing/ (Cached inputs are up to 4X cheaper)
# ==============================================================================
# Core Rules Tested:
# 1. Minimum Threshold: Prompts MUST be >= 1,024 tokens.
# 2. Exact Prefix Match: Static instructions/docs must be at the FRONT.
# 3. Cache Metrics: Read from `response.usage.prompt_tokens_details.cached_tokens`.
# 4. Cost Reduction: Verify discount in `_hidden_params['response_cost']`.
# ==============================================================================

import os
import sys
import io
import time
from dotenv import load_dotenv
import litellm
from litellm import completion, completion_cost

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

MODEL_NAME = "gpt-4o-mini"


def run_openai_prompt_caching_deepdive():
    print("=" * 75)
    print("⚡ [Lec 42: Day 1] DEEP-DIVE: OPENAI PROMPT CACHING VERIFICATION")
    print("   Reference: https://platform.openai.com/docs/guides/prompt-caching")
    print("=" * 75)

    # --------------------------------------------------------------------------
    # 1. Rule 1: Minimum Threshold Check (< 1,024 tokens = NO CACHE)
    # --------------------------------------------------------------------------
    print("\n🔍 [Test 1] Testing Short Prompt (< 1,024 tokens):")
    short_messages = [
        {"role": "system", "content": "You are a concise engineering mentor."},
        {"role": "user", "content": "Explain binary search in 2 sentences."}
    ]
    resp_short_1 = completion(model=MODEL_NAME, messages=short_messages)
    details_s1 = getattr(resp_short_1.usage, "prompt_tokens_details", None)
    cached_s1 = getattr(details_s1, "cached_tokens", 0) if details_s1 else 0
    print(f"   • Prompt Tokens: {resp_short_1.usage.prompt_tokens} (below 1,024 limit)")
    print(f"   • Cached Tokens: {cached_s1} -> (OpenAI only caches prompts >= 1,024 tokens)")

    # --------------------------------------------------------------------------
    # 2. Prepare Large Static Prefix (>= 1,024 tokens)
    # --------------------------------------------------------------------------
    # We load hamlet.txt (~40k tokens) or create a ~2,500 token static knowledge base.
    hamlet_path = os.path.join(CURRENT_DIR, "hamlet.txt")
    if os.path.exists(hamlet_path):
        with open(hamlet_path, "r", encoding="utf-8") as f:
            large_static_doc = f.read()[:20000] # ~5,000 tokens (plenty for >= 1024)
    else:
        # Fallback synthetic static manual
        large_static_doc = "Enterprise Architecture Specification:\n" + ("Guidelines and policies for microservices. " * 300)

    print(f"\n📦 [Test 2] Prepared Static Prefix Context (~{len(large_static_doc)//4:,} tokens)...")

    # --------------------------------------------------------------------------
    # 3. Call 1: Cold Cache (First Request -> Writes to OpenAI Cache)
    # --------------------------------------------------------------------------
    print("\n❄️  [Step A] Request 1 (Cold Cache) — Sending static prefix + Question 1...")
    messages_req1 = [
        {"role": "system", "content": f"Use this reference context:\n\n{large_static_doc}"},
        {"role": "user", "content": "Summarize the primary theme in 20 words."}
    ]

    t1 = time.time()
    resp_1 = completion(model=MODEL_NAME, messages=messages_req1)
    latency_1 = time.time() - t1

    prompt_tok_1 = resp_1.usage.prompt_tokens
    details_1 = getattr(resp_1.usage, "prompt_tokens_details", None)
    cached_tok_1 = getattr(details_1, "cached_tokens", 0) if details_1 else 0
    cost_1 = getattr(resp_1, "_hidden_params", {}).get("response_cost") or completion_cost(completion_response=resp_1)

    print(f"   • Latency:       {latency_1:.2f}s")
    print(f"   • Input Tokens:  {prompt_tok_1}")
    print(f"   • Cached Tokens: {cached_tok_1} (Cold run: 0 cached tokens)")
    print(f"   • Cost:          {cost_1 * 100:.4f} cents (${cost_1:.6f} USD)")

    # --------------------------------------------------------------------------
    # 4. Call 2: Warm Cache (Exact Prefix Match -> CACHE HIT!)
    # --------------------------------------------------------------------------
    print("\n🔥 [Step B] Request 2 (Warm Cache) — Exact same prefix + New Question 2...")
    messages_req2 = [
        messages_req1[0], # EXACT SAME static prefix
        {"role": "user", "content": "What is the tone of the opening paragraph in 10 words?"}
    ]

    t2 = time.time()
    resp_2 = completion(model=MODEL_NAME, messages=messages_req2)
    latency_2 = time.time() - t2

    prompt_tok_2 = resp_2.usage.prompt_tokens
    details_2 = getattr(resp_2.usage, "prompt_tokens_details", None)
    cached_tok_2 = getattr(details_2, "cached_tokens", 0) if details_2 else 0
    cost_2 = getattr(resp_2, "_hidden_params", {}).get("response_cost") or completion_cost(completion_response=resp_2)

    print(f"   • Latency:       {latency_2:.2f}s (Faster!)")
    print(f"   • Input Tokens:  {prompt_tok_2}")
    print(f"   • Cached Tokens: {cached_tok_2} (🎯 CACHE HIT! Tokens read from OpenAI cache)")
    print(f"   • Cost:          {cost_2 * 100:.4f} cents (${cost_2:.6f} USD)")

    # --------------------------------------------------------------------------
    # 5. Rule Verification & Math
    # --------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("📊 [OPENAI PROMPT CACHING VERIFICATION RESULTS]")
    print("=" * 75)
    print(f"1. Did OpenAI Cache the Prompt?    {'✅ YES' if cached_tok_2 > 0 else '❌ NO'}")
    print(f"2. Number of Cached Tokens:        {cached_tok_2:,} out of {prompt_tok_2:,}")
    if cost_1 > 0:
        savings = (1.0 - (cost_2 / cost_1)) * 100
        print(f"3. Realized Cost Savings:          {savings:.1f}% discount")
    print(f"4. Where in Response to Check:     response.usage.prompt_tokens_details.cached_tokens")
    print(f"5. Where in Cost to Check:         response._hidden_params['response_cost'] * 100")
    print("=" * 75)


if __name__ == "__main__":
    run_openai_prompt_caching_deepdive()
