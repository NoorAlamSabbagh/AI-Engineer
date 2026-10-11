# ==============================================================================
# Lec 42: Day 1 — Check Hamlet Baseline Call (Cells 59, 60, 61)
# File: MyPractice/week2/check_hamlet_gemini.py
# ==============================================================================

import os
import sys
import io
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows terminal
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# [Lec 42: Day 1] LiteLLM imports
import litellm
from litellm import completion

# LiteLLM looks for GEMINI_API_KEY for Google Gemini calls
google_key = os.getenv("GOOGLE_API_KEY")
if google_key and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = google_key

# Terminal vs Jupyter display helper:
try:
    from IPython import get_ipython
    if get_ipython() is not None:
        from IPython.display import Markdown, display
    else:
        def Markdown(x): return x
        def display(x): print(x)
except ImportError:
    def Markdown(x): return x
    def display(x): print(x)

def run_check():
    # --------------------------------------------------------------------------
    # Cell 59: Load Hamlet and find text snippet
    # --------------------------------------------------------------------------
    hamlet_path = os.path.join(CURRENT_DIR, "hamlet.txt")
    print(f"Reading: {hamlet_path}")
    with open(hamlet_path, "r", encoding="utf-8") as f:
        hamlet = f.read()

    loc = hamlet.find("Speak, man")
    print(f"Location found at index {loc}:")
    print("-" * 50)
    print(hamlet[loc : loc + 100])
    print("-" * 50)

    # --------------------------------------------------------------------------
    # Cell 60: Define the user question
    # --------------------------------------------------------------------------
    question = [{"role": "user", "content": "In Hamlet, when Laertes asks 'Where is my father?' what is the reply?"}]

    # --------------------------------------------------------------------------
    # Cell 61: Call completion() with Gemini (or fallback to OpenAI if Gemini key invalid)
    # --------------------------------------------------------------------------
    print("\nCalling completion()...")
    # [Lec 42: Day 1] In the lecture, Ed Donner demonstrated switching models via LiteLLM.
    # We default to 'gpt-4o-mini' for reliable, fast execution.
    chosen_model = "gpt-4o-mini"
    print(f"\nCalling completion() via LiteLLM model='{chosen_model}'...")
    response = completion(model=chosen_model, messages=question)

    print(f"\nResponse from [{chosen_model}]:")
    print("=" * 50)
    display(Markdown(response.choices[0].message.content))
    print("=" * 50)

    # Metrics from Cell 62
    print(f"\nInput tokens:  {response.usage.prompt_tokens}")
    print(f"Output tokens: {response.usage.completion_tokens}")
    print(f"Total tokens:  {response.usage.total_tokens}")
    cost = getattr(response, "_hidden_params", {}).get("response_cost")
    if cost is not None:
        print(f"Total cost:    {cost * 100:.4f} cents")

if __name__ == "__main__":
    run_check()
