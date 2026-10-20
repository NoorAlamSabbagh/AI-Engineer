"""
Week 2 • Day 3 — Building Chat UIs with Gradio: Your First Conversational AI Assistant (Lec 49–52)
===================================================================================================
Single unified practice script containing all Day 3 concepts from `llm_engineering-main/week2/day3.ipynb`:
1. Lab 1: Chatbot 101 Basics — Understanding `gr.ChatInterface(fn=chat)`.
2. Lab 2: Multi-Turn Memory Chat — Constructing the 'Memory Sandwich' with OpenAI.
3. Lab 3: Real-Time Chat Streaming — Word-by-word streaming using Python generators (`yield`).
4. Lab 4: Clothing Store Sales Assistant (Capstone) — Persona, sales promotion, and dynamic guardrails.
"""

import os
import sys
import io
from typing import Generator
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# UTF-8 encoding fix for Windows terminals
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Load environment variables
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key) if openai_api_key else None
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

MODEL_NAME = "gpt-4o-mini"


def format_history_for_openai(history: list) -> list:
    """
    Normalizes Gradio conversation history into OpenAI message schema:
    [{'role': 'user' | 'assistant', 'content': '...'}]
    Handles both modern dictionary format and legacy tuple pair format seamlessly.
    """
    messages = []
    for turn in history:
        if isinstance(turn, dict):
            messages.append({
                "role": turn.get("role", "user"),
                "content": str(turn.get("content", ""))
            })
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            user_msg, bot_msg = turn
            if user_msg:
                messages.append({"role": "user", "content": str(user_msg)})
            if bot_msg:
                messages.append({"role": "assistant", "content": str(bot_msg)})
    return messages


# =====================================================================
# LAB 1: CHATBOT 101 BASICS (Lec 49) — Understanding the Plumbing
# =====================================================================
def chat_basics_demo(message: str, history: list) -> str:
    """
    Lab 1 (Lec 49) demonstrates how Gradio's ChatInterface passes arguments:
    - message: The latest text typed by the user (string).
    - history: A list of prior conversation turns.
    """
    turn_num = len(history) + 1
    return (
        f"🤖 [Echo Bot (Lec 49) — Turn #{turn_num}]\n\n"
        f"• You just said: \"{message}\"\n"
        f"• Prior history items received: {len(history)}\n\n"
        f"💡 In Lab 2 (Lec 50), we will bundle this history and send it to OpenAI so the AI remembers earlier turns!"
    )


lab1_interface = gr.ChatInterface(
    fn=chat_basics_demo,
    title="🧪 Lab 1: Chatbot 101 Basics (Lec 49)",
    description="[Lec 49] Inspect how `(message, history)` works under the hood. Type anything to see how Gradio tracks history turns.",
    examples=["Hello there!", "What was my first message?", "How many messages have we sent?"],
    flagging_mode="never"
)


# =====================================================================
# LAB 2: MULTI-TURN MEMORY CHAT (Lec 50) — The Memory Sandwich
# =====================================================================
LAB2_SYSTEM_PROMPT = (
    "You are a helpful, witty, and concise AI tutor. "
    "Always remember the user's name and previous details mentioned during this chat session."
)

def chat_with_memory(message: str, history: list) -> str:
    """
    Lab 2 (Lec 50) constructs the 'Memory Sandwich':
    [System Message] + [Past History List] + [New User Message]
    and sends the complete bundle to OpenAI.
    """
    if not client or not openai_api_key:
        return "❌ OpenAI API key is missing in your .env file! Please set `OPENAI_API_KEY`."

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": LAB2_SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content or "No response received."
    except Exception as e:
        return f"❌ Error: {str(e)}"


lab2_interface = gr.ChatInterface(
    fn=chat_with_memory,
    title="🧠 Lab 2: Multi-Turn Memory Chat (Lec 50)",
    description="[Lec 50] Test conversational memory across multiple turns. Notice how the AI remembers context from your earlier messages!",
    examples=[
        "My favorite fruit is Mango and I live in Tokyo.",
        "What fruit did I say I like?",
        "Where do I live?"
    ],
    flagging_mode="never"
)


# =====================================================================
# LAB 3: REAL-TIME TOKEN STREAMING CHAT (Lec 51) — The `yield` Generator
# =====================================================================
def chat_stream(message: str, history: list) -> Generator[str, None, None]:
    """
    Lab 3 (Lec 51) streams tokens in real-time inside `gr.ChatInterface` using `yield`.
    Creates the smooth ChatGPT typewriter animation!
    """
    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": "You are a helpful AI assistant that explains concepts using clear, structured Markdown."}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    # Option A: Try local Ollama if OpenAI key is not set
    if not client or not openai_api_key:
        try:
            stream = ollama_client.chat.completions.create(
                model="llama3.2",
                messages=messages,
                stream=True
            )
            accumulated = ""
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                accumulated += token
                yield accumulated
            return
        except Exception as e:
            yield f"⚠️ OpenAI key missing and Ollama not reachable: {e}"
            return

    # Option B: OpenAI streaming
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            temperature=0.7
        )
        accumulated = ""
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            accumulated += token
            yield accumulated
    except Exception as e:
        yield f"❌ Streaming Error: {str(e)}"


lab3_interface = gr.ChatInterface(
    fn=chat_stream,
    title="⚡ Lab 3: Real-Time Streaming Chat (Lec 51)",
    description="[Lec 51] Live word-by-word typewriter streaming inside chat bubbles using Python's `yield` generator.",
    examples=[
        "Explain quantum computing in 3 simple bullet points.",
        "Write a short, inspiring 4-line poem about coding.",
        "Compare Python lists vs tuples with a quick example."
    ],
    flagging_mode="never"
)


# =====================================================================
# LAB 4: CLOTHING STORE SALES ASSISTANT (Lec 52 Capstone)
# =====================================================================
BASE_STORE_SYSTEM_PROMPT = (
    "You are a friendly, enthusiastic sales assistant in a trendy clothing store. "
    "Current Store Promotion Rules:\n"
    "• Hats are on super clearance at 60% OFF!\n"
    "• Most other clothing items are 50% OFF.\n"
    "• Shoes are NOT on sale today.\n\n"
    "Key Guidelines:\n"
    "1. Gently steer customers toward trying on items that are on sale.\n"
    "2. If the customer is unsure what to get, strongly encourage them to check out hats.\n"
    "3. If the customer asks for shoes, politely explain shoes are not on sale today, but remind them to look at hats!\n"
    "4. Keep replies natural, courteous, and concise (2-4 sentences max)."
)

def chat_clothing_store(message: str, history: list) -> Generator[str, None, None]:
    """
    Lab 4 (Lec 52 Capstone) conversational agent implementing:
    1. Persona-driven sales promotion (hats 60% off).
    2. Negative objection handling (shoes not on sale).
    3. Dynamic context injection: if user asks about 'belt', dynamically injects
       a store constraint that belts are out of stock / not sold!
    """
    clean_history = format_history_for_openai(history)

    # Dynamic Context Injection (Precursor to RAG & Guardrails!)
    active_system_prompt = BASE_STORE_SYSTEM_PROMPT
    if "belt" in message.lower():
        active_system_prompt += (
            "\n[SPECIAL INSTRUCTION]: The store does NOT sell belts at all. "
            "If the customer asks for belts, inform them politely and recommend other items that ARE on sale (especially hats!)."
        )

    messages = (
        [{"role": "system", "content": active_system_prompt}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    if not client or not openai_api_key:
        yield "❌ OpenAI API key is missing in your .env file!"
        return

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            temperature=0.7
        )
        accumulated = ""
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            accumulated += token
            yield accumulated
    except Exception as e:
        yield f"❌ Error: {str(e)}"


lab4_interface = gr.ChatInterface(
    fn=chat_clothing_store,
    title="👔 Lab 4: Clothing Store Sales Assistant (Lec 52)",
    description=(
        "[Lec 52 Capstone] An AI sales assistant with real business rules: 60% off hats, 50% off other items, "
        "shoe guardrail (not on sale), and dynamic detection of out-of-stock items (belts)!"
    ),
    examples=[
        "Hi! What deals do you have going on today?",
        "I need a new pair of running shoes.",
        "Do you have any leather belts in stock?",
        "I'm looking for a nice warm hat for winter."
    ],
    flagging_mode="never"
)


# =====================================================================
# UNIFIED DAY 3 MASTER DASHBOARD (Lec 49–52)
# =====================================================================
app = gr.TabbedInterface(
    interface_list=[
        lab1_interface,
        lab2_interface,
        lab3_interface,
        lab4_interface
    ],
    tab_names=[
        "🧪 1. Chatbot Basics (Lec 49)",
        "🧠 2. Memory Chat (Lec 50)",
        "⚡ 3. Live Streaming (Lec 51)",
        "👔 4. Store Assistant (Lec 52)"
    ],
    title="🎓 Week 2 • Day 3 — Building Chat UIs with Gradio (Lec 49–52)"
)


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("🌟 Week 2 • Day 3 (Lec 49–52) — Conversational AI Master Suite")
    print("=" * 65)
    print("📍 Local URL: http://127.0.0.1:7860")
    print("🌐 Opening automatically in your default browser...")
    print("Press Ctrl+C anytime to stop the server.")
    print("=" * 65 + "\n")

    app.launch(inbrowser=True, server_port=7860)
