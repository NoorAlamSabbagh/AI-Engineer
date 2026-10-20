"""
Week 2 • Day 5 — Agentic AI, Multi-Tool Workflows & Frontier SVG (Lec 57–61)
=============================================================================
Single unified practice script containing all Day 5 concepts from `llm_engineering-main/week2/day5.ipynb` & `extra.ipynb`:
1. Tab 1: The Gradio UI Hierarchy (Lec 57) — Comparing `Interface`, `ChatInterface`, and `Blocks`.
2. Tab 2: Multi-Modal Tools: Artist & Voice (Lec 58) — DALL-E image generation + TTS audio synthesis.
3. Tab 3: Agentic Workflow Engine (Lec 59) — Multi-tool coordination & city extraction.
4. Tab 4: FlightAI Grand Capstone (Lec 60) — Full custom `gr.Blocks` with Chatbot, Audio, and Vacation Postcards.
5. Tab 5: Special Extra: Frontier SVG Artist & Revealer (Lec 61) — Simon Willison's SVG AI benchmark & animated keyframes.
"""

import os
import sys
import io
import time
import json
import base64
import sqlite3
import tempfile
from datetime import datetime
from io import BytesIO
from typing import Generator, Tuple, Optional
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
from openai import OpenAI
from revealer import create_animated_svg, clean_svg_markup

# UTF-8 encoding fix for Windows terminals
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Load environment variables
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None
openrouter_client = (
    OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)
    if openrouter_api_key
    else None
)
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

MODEL_NAME = "gpt-4o-mini"
DB_PATH = os.path.join(os.path.dirname(__file__), "prices.db")

SYSTEM_MESSAGE = """
You are a helpful, courteous customer support assistant for an airline called FlightAI.
Give short, friendly answers, no more than 2 sentences.
Always be accurate. When asked for ticket prices, use your available tools.
If you don't know the answer and have no tool for it, say so politely.
"""


# =====================================================================
# SQLITE DATABASE INITIALIZATION (Day 5)
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


def get_ticket_price(city: str) -> str:
    """Queries SQLite database for ticket price."""
    clean_city = city.strip().lower()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM prices WHERE city = ?", (clean_city,))
        row = cursor.fetchone()
        if row:
            return f"The return flight ticket price to {city.title()} is ${row[0]:.2f}."
        return f"No price data available for {city.title()}."


price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]


# =====================================================================
# MULTI-MODAL TOOLS: ARTIST & TALKER (Lec 58)
# =====================================================================
def create_fallback_postcard(city: str) -> Image.Image:
    """Generates a clean local pop-art fallback postcard if API/quota is unavailable."""
    img = Image.new("RGB", (600, 600), color=(30, 41, 59))
    draw = ImageDraw.Draw(img)
    # Draw decorative frames
    draw.rectangle([20, 20, 580, 580], outline=(56, 189, 248), width=4)
    draw.rectangle([35, 35, 565, 565], outline=(244, 114, 182), width=2)
    # Add text
    draw.text((80, 180), "✈️ FlightAI Vacation Postcard", fill=(248, 250, 252))
    draw.text((80, 260), f"WELCOME TO {city.upper()}!", fill=(56, 189, 248))
    draw.text((80, 340), "✨ Pop-Art Style Travel Destination", fill=(226, 232, 240))
    draw.text((80, 420), "Explore iconic landmarks & unforgettable sights.", fill=(148, 163, 184))
    return img


def artist(city: str) -> Optional[Image.Image]:
    """Generates a vibrant pop-art vacation postcard using OpenAI DALL-E / Image API."""
    if not client or not openai_api_key:
        return create_fallback_postcard(city)

    prompt = (
        f"An image representing a vacation in {city}, showing tourist spots and everything "
        f"unique about {city}, in a vibrant, colorful pop-art travel poster style."
    )
    try:
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
            response_format="b64_json"
        )
        image_base64 = image_response.data[0].b64_json
        image_data = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_data))
    except Exception as e:
        print(f"⚠️ Image generation notice ({e}); using high-res postcard fallback.", flush=True)
        return create_fallback_postcard(city)


def talker(message: str) -> Optional[str]:
    """Generates audio speech using OpenAI TTS API and returns path to temp audio file."""
    if not client or not openai_api_key:
        return None

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Voices: onyx, alloy, coral, echo, fable, nova, shimmer
            input=message
        )
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(response.content)
        temp_audio.close()
        return temp_audio.name
    except Exception as e:
        print(f"⚠️ TTS audio generation notice ({e}).", flush=True)
        return None


def format_history_for_openai(history: list) -> list:
    """Normalizes conversation history into OpenAI message schema."""
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
# TAB 1: THE GRADIO UI HIERARCHY (Lec 57)
# =====================================================================
with gr.Blocks() as tab1_hierarchy:
    gr.Markdown(
        """
        # 🧩 The 3 Types of Gradio UIs Explained (Lec 57)
        In Week 2, you learned all three fundamental levels of Gradio:

        | UI Type | Purpose | How Much Control You Have | Where We Used It |
        | :--- | :--- | :---: | :--- |
        | **`gr.Interface`** | Simple single-shot apps (Input $\\to$ Output) | Low (turnkey) | Day 2 (Text transformations) |
        | **`gr.ChatInterface`** | Turnkey chat interfaces | Medium | Day 3 & 4 (Conversational assistants) |
        | **`gr.Blocks`** | **Complete custom control** | **Maximum (Pro)** | **Day 5 (Multi-modal layout & event chains)** |

        ---
        ### 💡 Why `gr.Blocks` is essential for Agentic AI:
        `gr.Blocks` allows you to arrange layouts side-by-side (using `gr.Row()` and `gr.Column()`),
        add multimedia outputs (like `gr.Image` and `gr.Audio`), and chain callbacks with `.then()`.
        """
    )


# =====================================================================
# TAB 2: MULTI-MODAL TOOLS: ARTIST & VOICE (Lec 58)
# =====================================================================
with gr.Blocks() as tab2_multimodal:
    gr.Markdown("### 🎨 Multi-Modal Generators: Artist & Voice Synthesizer (Lec 58)")
    with gr.Row():
        with gr.Column():
            gr.Markdown("#### 🖼️ Tool 1: Vacation Postcard Artist (`artist`)")
            city_input = gr.Textbox(label="Destination City", value="Paris", placeholder="e.g. Paris, Tokyo, London")
            art_btn = gr.Button("🎨 Paint Vacation Postcard", variant="primary")
            art_output = gr.Image(label="Generated Postcard", height=400)
            art_btn.click(fn=artist, inputs=city_input, outputs=art_output)

        with gr.Column():
            gr.Markdown("#### 🎙️ Tool 2: Voice Speech Synthesizer (`talker`)")
            text_input = gr.Textbox(
                label="Message to Speak",
                value="Welcome aboard FlightAI! A return ticket to Paris is currently $899.00.",
                lines=3
            )
            voice_btn = gr.Button("🔊 Speak Out Loud", variant="primary")
            audio_output = gr.Audio(label="Synthesized Speech (Onyx Voice)", autoplay=True)
            voice_btn.click(fn=talker, inputs=text_input, outputs=audio_output)


# =====================================================================
# TAB 3: AGENTIC WORKFLOW ENGINE (Lec 59 — Multi-Tool Coordination)
# =====================================================================
def handle_tool_calls_and_return_cities(assistant_message) -> Tuple[list, list]:
    """Executes database tools and tracks destination cities for multi-modal generation."""
    responses = []
    cities = []
    for tool_call in assistant_message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get("destination_city", "")
            if city:
                cities.append(city)
            price_details = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
    return responses, cities


def chat_agent_engine(message: str, history: list) -> str:
    """Agentic reasoning engine resolving database fares and tracking cities."""
    if not client or not openai_api_key:
        return "❌ OpenAI API key is missing in your .env file!"

    clean_history = format_history_for_openai(history)
    messages = (
        [{"role": "system", "content": SYSTEM_MESSAGE}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    log_trace = []

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            temperature=0.2
        )

        loop_count = 0
        while response.choices[0].finish_reason == "tool_calls" and loop_count < 5:
            loop_count += 1
            assistant_msg = response.choices[0].message
            tool_responses, cities = handle_tool_calls_and_return_cities(assistant_msg)

            for city in cities:
                fare = get_ticket_price(city)
                log_trace.append(f"• Tool Execution: `{city.title()}` ➔ {fare}")

            messages.append(assistant_msg)
            messages.extend(tool_responses)

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                temperature=0.2
            )

        reply = response.choices[0].message.content
        trace_str = ""
        if log_trace:
            trace_str = "\n\n---\n**🤖 Agentic Workflow Tool Log:**\n" + "\n".join(log_trace)
        return reply + trace_str
    except Exception as e:
        return f"❌ Error: {str(e)}"


tab3_engine = gr.ChatInterface(
    fn=chat_agent_engine,
    title="🗄️ Tab 3: Agentic Workflow Engine (Lec 59)",
    description=(
        "[Lec 59 Agentic Engine] Ask about flight fares. "
        "The agent dynamically calls the SQLite tool, extracts destination cities, and prepares multi-modal payloads."
    ),
    examples=[
        "How much is a return flight to Tokyo?",
        "What are the ticket prices for Paris and London?",
        "Can I fly to Sydney?"
    ],
    flagging_mode="never"
)


# =====================================================================
# TAB 4: FLIGHTAI GRAND CAPSTONE (Lec 60 — Custom Multi-Modal Blocks)
# =====================================================================
def put_message_in_chatbot(user_message: str, history: list):
    """Step 1 in event chain: Immediately adds user's message to chat bubbles and clears text input."""
    if not user_message.strip():
        return "", history
    new_history = history + [{"role": "user", "content": user_message}]
    return "", new_history


def chat_multimodal_agent(history: list):
    """
    Step 2 in event chain:
    1. Runs LLM with SQLite tool calling via `while` loop.
    2. Generates TTS voice audio via `talker()`.
    3. If a city was queried, paints a vibrant pop-art postcard via `artist()`!
    """
    if not history:
        return history, None, None

    clean_history = format_history_for_openai(history)
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}] + clean_history

    cities = []
    postcard = None
    voice_audio = None

    if not client or not openai_api_key:
        error_msg = "❌ OpenAI API key is missing in your .env file!"
        history.append({"role": "assistant", "content": error_msg})
        return history, None, None

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            temperature=0.2
        )

        while response.choices[0].finish_reason == "tool_calls":
            assistant_msg = response.choices[0].message
            tool_responses, found_cities = handle_tool_calls_and_return_cities(assistant_msg)
            cities.extend(found_cities)
            messages.append(assistant_msg)
            messages.extend(tool_responses)

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                temperature=0.2
            )

        reply_text = response.choices[0].message.content or "Thank you for contacting FlightAI!"
        history.append({"role": "assistant", "content": reply_text})

        # Multi-modal output 1: Voice synthesis
        voice_audio = talker(reply_text)

        # Multi-modal output 2: Vacation postcard
        if cities:
            postcard = artist(cities[0])

        return history, voice_audio, postcard
    except Exception as e:
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        return history, None, None


with gr.Blocks() as tab4_capstone:
    gr.Markdown(
        """
        # 🌟 FlightAI Multi-Modal Customer Support Assistant (Lec 60 Grand Capstone)
        **A complete Agentic AI Workflow:**
        1. **SQLite Database Tool**: Automatically checks live ticket prices.
        2. **AI Voice Synthesis**: Speaks the answer out loud with OpenAI TTS.
        3. **Pop-Art Vacation Postcard**: Paints an image of the destination city!
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            chatbot_ui = gr.Chatbot(height=480, label="FlightAI Concierge")
        with gr.Column(scale=1):
            image_output_ui = gr.Image(label="🎨 Tourist Vacation Postcard", height=480)

    with gr.Row():
        audio_output_ui = gr.Audio(label="🔊 Spoken Voice Response", autoplay=True)

    with gr.Row():
        msg_input_ui = gr.Textbox(
            label="Chat with our FlightAI Assistant:",
            placeholder="e.g. How much is a return flight to Paris? (Press Enter)",
            scale=4
        )
        submit_btn_ui = gr.Button("🚀 Send", variant="primary", scale=1)

    gr.Examples(
        examples=[
            "How much is a return flight to Paris?",
            "What is the ticket price for Tokyo?",
            "Can you tell me the fare to London?"
        ],
        inputs=msg_input_ui
    )

    # Event chaining using .then()
    msg_input_ui.submit(
        put_message_in_chatbot,
        inputs=[msg_input_ui, chatbot_ui],
        outputs=[msg_input_ui, chatbot_ui]
    ).then(
        chat_multimodal_agent,
        inputs=chatbot_ui,
        outputs=[chatbot_ui, audio_output_ui, image_output_ui]
    )

    submit_btn_ui.click(
        put_message_in_chatbot,
        inputs=[msg_input_ui, chatbot_ui],
        outputs=[msg_input_ui, chatbot_ui]
    ).then(
        chat_multimodal_agent,
        inputs=chatbot_ui,
        outputs=[chatbot_ui, audio_output_ui, image_output_ui]
    )


# =====================================================================
# TAB 5: SPECIAL EXTRA — FRONTIER SVG ARTIST & REVEALER (Lec 61)
# =====================================================================
SAMPLE_PELICAN_SVG = """<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:12px; width:100%; max-height:420px;">
  <circle cx="100" cy="220" r="45" fill="none" stroke="#38bdf8" stroke-width="5"/>
  <circle cx="100" cy="220" r="8" fill="#38bdf8"/>
  <circle cx="280" cy="220" r="45" fill="none" stroke="#38bdf8" stroke-width="5"/>
  <circle cx="280" cy="220" r="8" fill="#38bdf8"/>
  <line x1="100" y1="220" x2="180" y2="220" stroke="#f43f5e" stroke-width="6"/>
  <line x1="180" y1="220" x2="260" y2="150" stroke="#f43f5e" stroke-width="6"/>
  <line x1="100" y1="220" x2="160" y2="140" stroke="#f43f5e" stroke-width="6"/>
  <line x1="160" y1="140" x2="260" y2="150" stroke="#f43f5e" stroke-width="6"/>
  <line x1="180" y1="220" x2="150" y2="120" stroke="#f43f5e" stroke-width="6"/>
  <ellipse cx="145" cy="115" rx="20" ry="6" fill="#e2e8f0"/>
  <line x1="260" y1="150" x2="275" y2="110" stroke="#f43f5e" stroke-width="6"/>
  <line x1="260" y1="110" x2="290" y2="110" stroke="#94a3b8" stroke-width="6"/>
  <ellipse cx="180" cy="110" rx="40" ry="28" fill="#f8fafc"/>
  <path d="M 195 100 Q 230 70 240 50" fill="none" stroke="#f8fafc" stroke-width="18" stroke-linecap="round"/>
  <circle cx="245" cy="45" r="16" fill="#f8fafc"/>
  <circle cx="249" cy="42" r="3" fill="#0f172a"/>
  <path d="M 252 46 L 330 65 Q 290 85 248 55 Z" fill="#f59e0b"/>
  <path d="M 260 62 Q 295 95 248 70 Z" fill="#d97706" opacity="0.6"/>
  <path d="M 160 115 Q 190 145 160 140 Z" fill="#cbd5e1"/>
  <line x1="170" y1="125" x2="185" y2="200" stroke="#f59e0b" stroke-width="5"/>
  <line x1="185" y1="200" x2="195" y2="205" stroke="#f59e0b" stroke-width="5"/>
</svg>"""

SAMPLE_PANDA_SVG = """<svg viewBox="0 0 400 320" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:12px; width:100%; max-height:420px;">
  <ellipse cx="200" cy="150" rx="55" ry="65" fill="#f8fafc"/>
  <path d="M 155 120 Q 200 135 245 120 Q 250 170 200 175 Q 150 170 155 120 Z" fill="#1e293b"/>
  <circle cx="200" cy="80" r="42" fill="#f8fafc"/>
  <circle cx="168" cy="50" r="14" fill="#0f172a"/>
  <circle cx="232" cy="50" r="14" fill="#0f172a"/>
  <ellipse cx="185" cy="78" rx="8" ry="12" fill="#0f172a" transform="rotate(-15 185 78)"/>
  <ellipse cx="215" cy="78" rx="8" ry="12" fill="#0f172a" transform="rotate(15 215 78)"/>
  <circle cx="186" cy="76" r="3" fill="#ffffff"/>
  <circle cx="214" cy="76" r="3" fill="#ffffff"/>
  <ellipse cx="200" cy="90" rx="6" ry="4" fill="#0f172a"/>
  <path d="M 194 95 Q 200 100 206 95" stroke="#0f172a" stroke-width="2" fill="none"/>
  <rect x="235" y="130" width="30" height="22" rx="4" fill="#854d0e"/>
  <line x1="245" y1="130" x2="255" y2="130" stroke="#a16207" stroke-width="3"/>
  <line x1="220" y1="125" x2="240" y2="135" stroke="#1e293b" stroke-width="12" stroke-linecap="round"/>
  <line x1="180" y1="125" x2="160" y2="145" stroke="#1e293b" stroke-width="12" stroke-linecap="round"/>
  <line x1="185" y1="205" x2="170" y2="250" stroke="#1e293b" stroke-width="14" stroke-linecap="round"/>
  <line x1="215" y1="205" x2="235" y2="250" stroke="#1e293b" stroke-width="14" stroke-linecap="round"/>
  <rect x="150" y="250" width="35" height="15" rx="5" fill="#f43f5e"/>
  <circle cx="156" cy="272" r="7" fill="#38bdf8"/>
  <circle cx="174" cy="272" r="7" fill="#38bdf8"/>
  <rect x="225" y="250" width="35" height="15" rx="5" fill="#f43f5e"/>
  <circle cx="231" cy="272" r="7" fill="#38bdf8"/>
  <circle cx="249" cy="272" r="7" fill="#38bdf8"/>
</svg>"""


def generate_and_reveal_svg(challenge: str, model_option: str, step_delay: float):
    """Generates an SVG using the chosen provider/model and animates it with CSS keyframes."""
    challenge = challenge.strip() if challenge else "a pelican riding a bicycle"
    start_time = datetime.now()

    # Instant pre-computed demos
    if "Instant Demo (Pelican)" in model_option:
        animated_svg = create_animated_svg(SAMPLE_PELICAN_SVG, step_delay=step_delay)
        stats = f"⚡ **Mode:** Pre-computed Benchmark • **Challenge:** Pelican on a bicycle • **Animation Delay:** {step_delay}s/element"
        html_card = f"""
        <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:18px; text-align:center;">
            <div style="color:#38bdf8; font-weight:600; margin-bottom:12px; font-size:14px;">🌟 Simon Willison's Legendary Benchmark (Pelican riding a bicycle)</div>
            {animated_svg}
        </div>
        """
        return html_card, stats, SAMPLE_PELICAN_SVG

    if "Instant Demo (Panda)" in model_option:
        animated_svg = create_animated_svg(SAMPLE_PANDA_SVG, step_delay=step_delay)
        stats = f"⚡ **Mode:** Pre-computed Benchmark • **Challenge:** Panda rollerblading to work • **Animation Delay:** {step_delay}s/element"
        html_card = f"""
        <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:18px; text-align:center;">
            <div style="color:#4ade80; font-weight:600; margin-bottom:12px; font-size:14px;">🐼 Course day5.ipynb Challenge: Panda Rollerblading to Work</div>
            {animated_svg}
        </div>
        """
        return html_card, stats, SAMPLE_PANDA_SVG

    prompt = (
        f"Generate an SVG of {challenge}. "
        "Respond with the SVG XML markup ONLY. "
        "Do not include explanations, DO NOT wrap in markdown backticks."
    )
    messages = [{"role": "user", "content": prompt}]
    raw_svg = ""
    used_model = model_option

    try:
        if "OpenAI" in model_option and client:
            target_model = "gpt-4o-mini" if "gpt-4o-mini" in model_option else "gpt-4o"
            response = client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.7
            )
            raw_svg = response.choices[0].message.content or ""
            used_model = f"OpenAI ({target_model})"

        elif "OpenRouter" in model_option and openrouter_client:
            # Extract target model or default to gpt-4o-mini
            target_model = "openai/gpt-4o-mini"
            response = openrouter_client.chat.completions.create(
                model=target_model,
                messages=messages
            )
            raw_svg = response.choices[0].message.content or ""
            used_model = f"OpenRouter ({target_model})"

        elif "Local Ollama" in model_option:
            response = ollama_client.chat.completions.create(
                model="llama3.2",
                messages=messages
            )
            raw_svg = response.choices[0].message.content or ""
            used_model = "Local Ollama (llama3.2)"

        else:
            # Fallback if no API key is active
            raw_svg = SAMPLE_PELICAN_SVG
            used_model = "Fallback (No live API key active; used Simon Willison's Pelican)"

    except Exception as e:
        print(f"⚠️ Live SVG generation failed: {e}. Falling back to sample SVG.", flush=True)
        raw_svg = SAMPLE_PANDA_SVG
        used_model = f"Fallback (Error: {str(e)[:60]}...)"

    raw_clean = clean_svg_markup(raw_svg)
    if not raw_clean:
        raw_clean = SAMPLE_PELICAN_SVG

    animated_svg = create_animated_svg(raw_clean, step_delay=step_delay)
    elapsed = (datetime.now() - start_time).total_seconds()

    stats_md = (
        f"⏱️ **Elapsed Time:** {elapsed:.2f}s | "
        f"🤖 **Model:** `{used_model}` | "
        f"📐 **Markup Length:** {len(raw_clean):,} characters | "
        f"✨ **Animation:** Staggered @ {step_delay}s per shape"
    )

    html_container = f"""
    <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:18px; text-align:center;">
        <div style="color:#e2e8f0; font-weight:600; margin-bottom:12px; font-size:14px;">
            🎨 Vector SVG Drawing: <span style="color:#38bdf8;">"{challenge}"</span>
        </div>
        {animated_svg}
    </div>
    """
    return html_container, stats_md, raw_clean


with gr.Blocks() as tab5_svg:
    gr.Markdown(
        """
        # 🎨 Special Extra: Frontier SVG Artist & Animated Revealer (Lec 61)
        **Inspired by Simon Willison's legendary AI Benchmark: *"Can frontier models draw a pelican riding a bicycle in SVG?"***
        
        ### 🧠 Why Generating an SVG is a Profound Test of Spatial Intelligence:
        1. **Not a Pixel Generator**: Unlike DALL-E or Midjourney, the LLM cannot "dream" pixels in a latent diffusion space.
        2. **Mathematical Geometry**: The model must calculate 2D Cartesian coordinates, radii, and Bézier curves (`<path d="...">`).
        3. **Physical & Anatomical Layout**: It must understand that bicycle wheels sit at the bottom, pedals connect to cranks, and the pelican's feet must reach the pedals with its wings holding handlebars!
        4. **Live Keyframe Revealer**: The generated SVG is parsed with Python `xml.etree.ElementTree` and injected with staggered `@keyframes reveal` CSS so each vector shape draws itself sequentially!
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            challenge_input = gr.Textbox(
                label="🎯 Drawing Challenge Prompt",
                value="a panda rollerblading to work",
                placeholder="e.g. a pelican riding a bicycle, a futuristic cybernetic owl, a cat playing chess..."
            )

            model_dropdown = gr.Dropdown(
                label="🤖 AI Model / Provider",
                choices=[
                    "Instant Demo (Pelican) — Simon Willison Benchmark",
                    "Instant Demo (Panda) — day5.ipynb Challenge",
                    "OpenAI (gpt-4o-mini)",
                    "OpenAI (gpt-4o)",
                    "Local Ollama (llama3.2)",
                    "OpenRouter (openai/gpt-4o-mini)"
                ],
                value="Instant Demo (Pelican) — Simon Willison Benchmark"
            )

            speed_slider = gr.Slider(
                label="⚡ Element Reveal Delay (seconds per shape)",
                minimum=0.01,
                maximum=0.30,
                step=0.01,
                value=0.08
            )

            svg_submit_btn = gr.Button("🚀 Generate & Animate SVG", variant="primary")

            gr.Examples(
                examples=[
                    ["a pelican riding a bicycle", "Instant Demo (Pelican) — Simon Willison Benchmark"],
                    ["a panda rollerblading to work", "Instant Demo (Panda) — day5.ipynb Challenge"],
                    ["a robot drinking coffee in a cafe", "OpenAI (gpt-4o-mini)"],
                    ["a sailboat navigating stormy neon waves", "OpenAI (gpt-4o-mini)"]
                ],
                inputs=[challenge_input, model_dropdown]
            )

        with gr.Column(scale=1):
            svg_preview_html = gr.HTML(
                label="Live Animated SVG Canvas",
                value="""
                <div style="background:#090d16; border:1px dashed #334155; border-radius:14px; padding:40px; text-align:center; color:#94a3b8;">
                    Click <b>Generate & Animate SVG</b> to watch the model's vector paths draw themselves live!
                </div>
                """
            )
            svg_stats_md = gr.Markdown("Ready to generate vector artwork.")

    with gr.Accordion("📜 View Raw Generated SVG XML Markup", open=False):
        raw_svg_display = gr.Code(label="SVG XML Markup", language="html")

    svg_submit_btn.click(
        generate_and_reveal_svg,
        inputs=[challenge_input, model_dropdown, speed_slider],
        outputs=[svg_preview_html, svg_stats_md, raw_svg_display]
    )


# =====================================================================
# UNIFIED DAY 5 MASTER DASHBOARD (Lec 57–61)
# =====================================================================
app = gr.TabbedInterface(
    interface_list=[
        tab1_hierarchy,
        tab2_multimodal,
        tab3_engine,
        tab4_capstone,
        tab5_svg
    ],
    tab_names=[
        "🧩 1. Gradio UI Hierarchy (Lec 57)",
        "🎨 2. Multi-Modal Generators (Lec 58)",
        "🗄️ 3. Agentic Workflow Engine (Lec 59)",
        "🌟 4. FlightAI Grand Capstone (Lec 60)",
        "🖌️ 5. Frontier SVG Artist & Revealer (Lec 61)"
    ],
    title="🎓 Week 2 • Day 5 — Agentic AI, Multi-Tool & Frontier SVG (Lec 57–61)"
)


if __name__ == "__main__":
    print("\n" + "=" * 75)
    print("🌟 Week 2 • Day 5 (Lec 57–61) — Agentic AI, Multi-Tool & Frontier SVG")
    print("=" * 75)
    print("📍 Local URL: http://127.0.0.1:7860")
    print("🌐 Opening automatically in your default browser...")
    print("Press Ctrl+C anytime to stop the server.")
    print("=" * 75 + "\n")

    app.launch(inbrowser=True, server_port=7860)
