# 🛠️ Week 2 • Day 4 — How LLM Tool Calling Really Works: No Magic, Just Prompts (Lec 53–56)

> **Welcome to Day 4!**  
> Today we demystify one of the most powerful capabilities of Frontier LLMs: **Tool Calling (Function Calling)**.  
> We build an **Airline AI Customer Support Assistant** for *FlightAI* that queries live ticket prices and modifies flight fares inside a real SQLite database!

---

## 🎩 The Big Myth: "Is the AI Running Code on My Computer?"

When beginners hear that an LLM can "call functions" or "query databases", they often imagine something spooky:
* *Myth*: The AI model has a Python interpreter inside its brain, reaches into your computer, and runs terminal commands or SQL queries.

### 💡 The Reality: "No Magic, Just Prompts & JSON!"
**An LLM can ONLY output text.** It cannot connect to your database. It cannot execute Python. It cannot press buttons.

So how does Tool Calling actually work? It is simply a polite 4-step conversation handshake:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   THE 4-STEP TOOL CALLING HANDSHAKE                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 👤 User asks        : "How much is a flight to London?"             │
│    🐍 Python sends     : User question + JSON description of tools     │
│                                                                        │
│ 2. 🤖 LLM responds     : "I cannot check prices myself, but please run │
│                          get_ticket_price(destination_city='london')   │
│                          with call_id='call_abc123' for me!"           │
│                                                                        │
│ 3. 🐍 Python executes  : Runs get_ticket_price('london') locally       │
│                          Database returns: "$799"                      │
│    🐍 Python sends back: {"role": "tool", "content": "$799",           │
│                          "tool_call_id": "call_abc123"}                │
│                                                                        │
│ 4. 🤖 LLM final reply  : "A return ticket to London is $799."          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 Step 1: Describing Your Tool (JSON Schema)

To let the model know what tools exist, you provide a JSON Schema dictionary describing:
1. `name`: What function to call.
2. `description`: When and why the AI should choose this tool.
3. `parameters`: What arguments the function expects and their data types.

```python
price_tool = {
    "type": "function",
    "function": {
        "name": "get_ticket_price",
        "description": "Get the current return flight ticket price for a destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The destination city name (e.g. London, Paris, Tokyo)"
                }
            },
            "required": ["destination_city"],
            "additionalProperties": False
        }
    }
}
```

---

## ⚡ Step 2: The Tool Calling Flow in Python

When calling OpenAI, you pass `tools=[price_tool]`:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# If the AI decided it needs a tool, finish_reason will be "tool_calls"
if response.choices[0].finish_reason == "tool_calls":
    tool_call = response.choices[0].message.tool_calls[0]
    
    # 1. Parse arguments chosen by the LLM
    args = json.loads(tool_call.function.arguments)
    city = args["destination_city"]
    
    # 2. Run the real function locally
    result = get_ticket_price(city)
    
    # 3. Append BOTH the assistant's request and the tool result
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "content": result,
        "tool_call_id": tool_call.id
    })
    
    # 4. Ask the LLM to write the final human response
    final_response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return final_response.choices[0].message.content
```

---

## 🚀 Step 3: Upgrading to Advanced Tool Calling

In Day 4, we level up the tool calling loop in 3 major ways:

### 1. Handling Multiple Tool Calls in One Message (Parallel Calling)
If the user asks: *"Compare flights to London and Tokyo"*, the model returns **two tool calls** in `message.tool_calls`. We iterate through all of them using a `for` loop.

### 2. Multi-Step Agentic Loops (`while` Loop)
What if tool #1 reveals information that prompts the AI to run tool #2?  
Instead of an `if` statement, we use a `while` loop:
```python
while response.choices[0].finish_reason == "tool_calls":
    # Keep executing tools until the model has everything it needs!
```

### 3. Real SQLite Database Integration (`prices.db`)
Instead of hardcoding a Python dictionary, we hook up a real SQLite database with:
* **Tool 1 (`get_ticket_price`)**: `SELECT price FROM prices WHERE city = ?`
* **Tool 2 (`set_ticket_price`)**: `INSERT INTO prices ... ON CONFLICT DO UPDATE` (Allows the AI to update prices when an airline manager requests it!).

---

## 📂 Day 4 Practice Architecture

All concepts from `day4.ipynb` are consolidated in:
- [**`practice.py`**](file:///d:/AlamProgrammingPractice/AI_LLM%20Engineer/MyPractice/week2/day4/practice.py) — Unified master dashboard featuring 4 interactive tabs:
  - **Tab 1: ✈️ Baseline Assistant (No Tools)** — Demonstrates how LLMs fail or hallucinate when asked for real-time prices without tools.
  - **Tab 2: 🛠️ In-Memory Tool Calling** — Single and parallel multi-city tool calling with raw JSON inspection.
  - **Tab 3: 🗄️ SQLite Database Tools** — Live relational database queries (`SELECT`) and price updates (`UPDATE`).
  - **Tab 4: 🤖 Full Autonomous Airline Agent (Capstone)** — Multi-turn `gr.ChatInterface` agent that can look up fares, compare cities, and update pricing policies dynamically.

---

## 💻 How to Run Day 4 Practice

Open your PowerShell terminal, activate your virtual environment, and run:

```powershell
cd "d:\AlamProgrammingPractice\AI_LLM Engineer\MyPractice"
.\.venv\Scripts\Activate.ps1

python week2/day4/practice.py
```

* Opens automatically in your default browser at **`http://127.0.0.1:7860`**.
* Try asking:
  - *"How much is a return flight to Tokyo?"*
  - *"Can you compare flight prices to London and Paris?"*
  - *"Update the ticket price for Sydney to $1850."*
  - *"What is the new price to Sydney now?"*
* Press `Ctrl+C` in your terminal to stop the server anytime.
