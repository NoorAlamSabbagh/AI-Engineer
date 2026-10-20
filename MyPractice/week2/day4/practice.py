"""
Week 2 • Day 4 — How LLM Tool Calling Really Works (No Magic, Just Prompts) (Lec 53–56)
========================================================================================
Single unified practice script containing all Day 4 concepts from `llm_engineering-main/week2/day4.ipynb`:
1. Tab 1: Baseline Airline Assistant (Lec 53) — Chatbot without tools (shows limitations/hallucination).
2. Tab 2: In-Memory Tool Calling (Lec 54) — JSON schema definition & parallel multi-tool calls.
3. Tab 3: SQLite Database Tools (Lec 55) — Relational database queries (`SELECT`) and fare updates (`UPDATE`).
4. Tab 4: Autonomous Airline Agent (Lec 56 Capstone) — Full multi-turn agent with `while` loop tool execution.
"""

import os
import sys
import io
import json
import sqlite3
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
DB_PATH = os.path.join(os.path.dirname(__file__), "prices.db")

AIRLINE_SYSTEM_PROMPT = """
You are a helpful, professional customer support assistant for an airline called FlightAI.
Guidelines:
1. Give short, courteous answers (1 to 2 sentences max).
2. Always be accurate.
3. When asked for ticket prices or to update prices, always use your available tools.
4. If you don't know the answer and have no tool for it, say so politely.
"""


# =====================================================================
# SQLITE DATABASE INITIALIZATION (Lec 55)
# =====================================================================
def init_database():
    """Initializes SQLite database with default flight fares."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)"
        )
        initial_fares = {
            "london": 799.0,
            "paris": 899.0,
            "tokyo": 1420.0,
            "sydney": 2999.0,
            "berlin": 499.0,
            "new york": 650.0
        }
        for city, price in initial_fares.items():
            cursor.execute(
                "INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?",
                (city.lower(), price, price)
            )
        conn.commit()

init_database()


def db_get_ticket_price(destination_city: str) -> str:
    """Queries SQLite database for destination ticket price."""
    clean_city = destination_city.strip().lower()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM prices WHERE city = ?", (clean_city,))
        row = cursor.fetchone()
        if row:
            return f"The return flight ticket price to {destination_city.title()} is ${row[0]:.2f}."
        return f"No flight price data available for {destination_city.title()}."


def db_set_ticket_price(destination_city: str, new_price: float) -> str:
    """Updates or inserts a flight ticket price in SQLite database."""
    clean_city = destination_city.strip().lower()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?",
            (clean_city, float(new_price), float(new_price))
        )
        conn.commit()
    return f"Successfully updated ticket price for {destination_city.title()} to ${new_price:.2f}."


def get_all_db_prices() -> list:
    """Fetches all fares from database for UI display."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT city, price FROM prices ORDER BY city ASC")
        return [[row[0].title(), f"${row[1]:.2f}"] for row in cursor.fetchall()]


# =====================================================================
# TOOL DEFINITIONS (JSON Schemas for OpenAI Function Calling)
# =====================================================================
tools_read_only = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "Get the current return flight ticket price for a destination city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination_city": {
                        "type": "string",
                        "description": "The destination city name (e.g. London, Paris, Tokyo, Sydney)"
                    }
                },
                "required": ["destination_city"],
                "additionalProperties": False
            }
        }
    }
]

tools_read_write = [
    tools_read_only[0],
    {
        "type": "function",
        "function": {
            "name": "set_ticket_price",
            "description": "Set or update the flight ticket price for a destination city in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination_city": {
                        "type": "string",
                        "description": "The destination city name (e.g. London, Paris, Sydney)"
                    },
                    "new_price": {
                        "type": "number",
                        "description": "The new return ticket price in US dollars"
                    }
                },
                "required": ["destination_city", "new_price"],
                "additionalProperties": False
            }
        }
    }
]


def format_history_for_openai(history: list) -> list:
    """Formats history list into standard OpenAI messages."""
    messages = []
    for turn in history:
        if isinstance(turn, dict):
            messages.append({"role": turn.get("role", "user"), "content": str(turn.get("content", ""))})
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            if turn[0]:
                messages.append({"role": "user", "content": str(turn[0])})
            if turn[1]:
                messages.append({"role": "assistant", "content": str(turn[1])})
    return messages


# =====================================================================
# TAB 1: BASELINE AIRLINE ASSISTANT (Lec 53 — No Tools)
# =====================================================================
def chat_baseline(message: str, history: list) -> str:
    """Baseline chatbot without tools — demonstrates lack of live knowledge."""
    if not client or not openai_api_key:
        return "❌ OpenAI API key is missing in your .env file!"

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": AIRLINE_SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content or "No response."
    except Exception as e:
        return f"❌ Error: {str(e)}"


tab1_interface = gr.ChatInterface(
    fn=chat_baseline,
    title="✈️ Tab 1: Baseline Assistant (Lec 53 — No Tools)",
    description=(
        "[Lec 53 Baseline] Ask for flight prices to Tokyo or London. "
        "Notice the model either admits it doesn't know real-time prices or makes them up, because it has NO tools!"
    ),
    examples=[
        "What is the flight ticket price to Tokyo?",
        "Can I fly to Paris?",
        "What airlines do you partner with?"
    ],
    flagging_mode="never"
)


# =====================================================================
# TAB 2: IN-MEMORY TOOL CALLING (Lec 54 — Single & Parallel Calls)
# =====================================================================
memory_prices = {"london": "$799", "paris": "$899", "tokyo": "$1420", "sydney": "$2999"}

def chat_in_memory_tools(message: str, history: list) -> str:
    """Demonstrates single and parallel tool calling with audit logs."""
    if not client or not openai_api_key:
        return "❌ OpenAI API key is missing in your .env file!"

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": AIRLINE_SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    log_trace = []

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools_read_only,
            temperature=0.2
        )

        # Check if model requested tool call(s)
        if response.choices[0].finish_reason == "tool_calls":
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            for tool_call in assistant_msg.tool_calls:
                call_id = tool_call.id
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                city = args.get("destination_city", "")

                price = memory_prices.get(city.lower(), "Unknown ticket price")
                result_str = f"The price of a return ticket to {city.title()} is {price}."

                log_trace.append(f"🛠️ [Tool Executed]: `{func_name}(city='{city}')` ➔ Result: {price}")

                messages.append({
                    "role": "tool",
                    "content": result_str,
                    "tool_call_id": call_id
                })

            # Second call to get final human-friendly response
            final_res = client.chat.completions.create(model=MODEL_NAME, messages=messages)
            ai_reply = final_res.choices[0].message.content

            trace_formatted = "\n\n---\n**Tool Execution Trace:**\n" + "\n".join(log_trace)
            return ai_reply + trace_formatted

        return response.choices[0].message.content or "No response."
    except Exception as e:
        return f"❌ Error: {str(e)}"


tab2_interface = gr.ChatInterface(
    fn=chat_in_memory_tools,
    title="🛠️ Tab 2: In-Memory Tool Calling (Lec 54)",
    description=(
        "[Lec 54 Parallel Tools] Ask about one city or multiple cities at once! "
        "Watch how the LLM triggers parallel `tool_calls` for London and Tokyo in a single turn."
    ),
    examples=[
        "How much is a ticket to London?",
        "Can you compare return ticket prices for Tokyo and Paris?",
        "What is the cheapest ticket among London, Paris, and Tokyo?"
    ],
    flagging_mode="never"
)


# =====================================================================
# TAB 3: SQLITE DATABASE TOOLS (Lec 55 — Read & Write)
# =====================================================================
def chat_sqlite_tools(message: str, history: list) -> str:
    """Executes tools against SQLite database with live read & update."""
    if not client or not openai_api_key:
        return "❌ OpenAI API key is missing in your .env file!"

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": AIRLINE_SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    log_trace = []

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools_read_write,
            temperature=0.2
        )

        if response.choices[0].finish_reason == "tool_calls":
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            for tool_call in assistant_msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name == "get_ticket_price":
                    city = args.get("destination_city", "")
                    tool_result = db_get_ticket_price(city)
                    log_trace.append(f"🔍 [DB SELECT]: `{city}` ➔ {tool_result}")
                elif func_name == "set_ticket_price":
                    city = args.get("destination_city", "")
                    new_price = args.get("new_price", 0.0)
                    tool_result = db_set_ticket_price(city, new_price)
                    log_trace.append(f"✍️ [DB UPDATE]: Set `{city}` to ${new_price:.2f}")
                else:
                    tool_result = f"Error: Unknown tool {func_name}"

                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call.id
                })

            final_res = client.chat.completions.create(model=MODEL_NAME, messages=messages)
            ai_reply = final_res.choices[0].message.content
            trace_formatted = "\n\n---\n**Database Audit Log:**\n" + "\n".join(log_trace)
            return ai_reply + trace_formatted

        return response.choices[0].message.content or "No response."
    except Exception as e:
        return f"❌ Error: {str(e)}"


with gr.Blocks() as tab3_blocks:
    gr.Markdown("### 🗄️ SQLite Database Tools (Read & Update Fares)")
    with gr.Row():
        with gr.Column(scale=2):
            tab3_chat = gr.ChatInterface(
                fn=chat_sqlite_tools,
                examples=[
                    "What is the flight price to Sydney?",
                    "Please update the ticket price for Sydney to $1750.",
                    "What is the new ticket price to Sydney now?"
                ],
                flagging_mode="never"
            )
        with gr.Column(scale=1):
            gr.Markdown("#### 📊 Current SQLite `prices.db` Table")
            db_table = gr.Dataframe(
                headers=["Destination City", "Ticket Price"],
                value=get_all_db_prices,
                interactive=False,
                label="Live Database Records"
            )
            refresh_btn = gr.Button("🔄 Refresh Database Table")
            refresh_btn.click(fn=get_all_db_prices, outputs=db_table)


# =====================================================================
# TAB 4: AUTONOMOUS AIRLINE AGENT (Lec 56 Capstone — `while` loop)
# =====================================================================
def run_autonomous_agent(message: str, history: list) -> Generator[str, None, None]:
    """
    Capstone multi-step agent using a `while` loop:
    Repeatedly executes tools until the LLM finishes reasoning and produces final answer.
    """
    if not client or not openai_api_key:
        yield "❌ OpenAI API key is missing in your .env file!"
        return

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": AIRLINE_SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    steps_log = []
    max_loops = 5
    loop_count = 0

    yield "🤔 Thinking and checking available airline tools..."

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools_read_write,
            temperature=0.2
        )

        while response.choices[0].finish_reason == "tool_calls" and loop_count < max_loops:
            loop_count += 1
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            for tool_call in assistant_msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name == "get_ticket_price":
                    city = args.get("destination_city", "")
                    tool_result = db_get_ticket_price(city)
                    steps_log.append(f"• Loop {loop_count}: Read fare for `{city.title()}` ➔ {tool_result}")
                elif func_name == "set_ticket_price":
                    city = args.get("destination_city", "")
                    new_price = args.get("new_price", 0.0)
                    tool_result = db_set_ticket_price(city, new_price)
                    steps_log.append(f"• Loop {loop_count}: Updated fare for `{city.title()}` to `${new_price:.2f}`")
                else:
                    tool_result = f"Error: unknown tool {func_name}"

                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call.id
                })

            yield f"🔄 Executing tools (Loop #{loop_count})...\n\n" + "\n".join(steps_log)

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools_read_write,
                temperature=0.2
            )

        final_content = response.choices[0].message.content or "Completed."
        audit_trail = ""
        if steps_log:
            audit_trail = "\n\n---\n**🤖 Agentic Reasoning & Tool Steps:**\n" + "\n".join(steps_log)

        yield final_content + audit_trail
    except Exception as e:
        yield f"❌ Agent Error: {str(e)}"


tab4_interface = gr.ChatInterface(
    fn=run_autonomous_agent,
    title="🤖 Tab 4: Autonomous Airline Agent (Lec 56 Capstone)",
    description=(
        "[Lec 56 Capstone] Autonomous Agent powered by a `while` loop. "
        "It can perform multi-step reasoning, compare fares across cities, and update SQLite records."
    ),
    examples=[
        "What is the flight ticket to Berlin?",
        "Compare prices for Paris and London, and tell me the cheaper option.",
        "Set the price of tickets to Berlin to $420 and confirm the new fare.",
        "What is the flight to New York and Tokyo?"
    ],
    flagging_mode="never"
)


# =====================================================================
# UNIFIED DAY 4 MASTER DASHBOARD (Lec 53–56)
# =====================================================================
app = gr.TabbedInterface(
    interface_list=[
        tab1_interface,
        tab2_interface,
        tab3_blocks,
        tab4_interface
    ],
    tab_names=[
        "✈️ 1. Baseline (Lec 53)",
        "🛠️ 2. Parallel Tools (Lec 54)",
        "🗄️ 3. SQLite Tools (Lec 55)",
        "🤖 4. Autonomous Agent (Lec 56)"
    ],
    title="🎓 Week 2 • Day 4 — How LLM Tool Calling Really Works (Lec 53–56)"
)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🌟 Week 2 • Day 4 (Lec 53–56) — LLM Tool Calling Master Suite")
    print("=" * 70)
    print("📍 Local URL: http://127.0.0.1:7860")
    print("🌐 Opening automatically in your default browser...")
    print("Press Ctrl+C anytime to stop the server.")
    print("=" * 70 + "\n")

    app.launch(inbrowser=True, server_port=7860)
