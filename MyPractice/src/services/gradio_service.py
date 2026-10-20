# ==============================================================================
# Lec 44–48: Day 2 — Gradio Web User Interfaces & Frontends
# File: src/services/gradio_service.py
# Description: Business logic for Day 2 text transformation, brochure generation,
#              and Gradio Tabbed Interface assembly for FastAPI mounting.
# ==============================================================================

import os
from typing import Generator
import requests
from bs4 import BeautifulSoup
import gradio as gr
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key) if openai_api_key else None
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

BROCHURE_SYSTEM_PROMPT = """
You are an elite corporate brand strategist and investment researcher.
Analyze the raw website landing page content and generate a polished, executive Markdown brochure for:
1. Prospective High-Value Customers
2. Venture Capital Investors
3. Top Engineering Candidates

Format with clear headers:
# 🏢 [Company Name] — Executive Overview
### 💡 The Core Problem & Value Proposition
### 🚀 Flagship Products & Key Capabilities
### 👥 Target Market & Customer Segments
### 🌟 Why Top Talent & Investors Should Care
### 📞 Call to Action / Next Steps
"""


def transform_text(user_text: str, mode: str) -> str:
    """Transforms input text based on the selected mode (Lec 44 & 45)."""
    if not user_text.strip():
        return "Please provide text to transform."

    if mode == "SHOUT (Uppercase)":
        return user_text.upper() + " 📢"
    elif mode == "whisper (lowercase)":
        return user_text.lower() + " 🤫"
    elif mode == "Reverse Text":
        return user_text[::-1] + " 🔄"
    elif mode == "Word & Character Count":
        words = len(user_text.split())
        chars = len(user_text)
        vowels = sum(1 for c in user_text.lower() if c in "aeiou")
        return f"📊 Text Statistics:\n• Words: {words}\n• Characters: {chars}\n• Vowels: {vowels}"
    return user_text


def scrape_website(url: str, max_chars: int = 3500) -> str:
    """Scrapes raw web page and cleans non-content tags."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=12)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input", "noscript", "svg", "nav", "footer"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return f"Page Title: {title}\n\nWeb Content:\n" + "\n".join(lines)[:max_chars]
    except Exception as e:
        return f"[Scrape Error: {e}]"


def generate_brochure_sync(company_name: str, url: str, model: str = "gpt-4o-mini") -> dict:
    """Synchronous brochure generation for FastAPI REST endpoint."""
    raw_content = scrape_website(url)
    if "[Scrape Error" in raw_content:
        return {
            "error": raw_content,
            "scraped_chars": 0,
            "brochure": f"Could not scrape {url}: {raw_content}"
        }

    user_prompt = (
        f"Company Name: {company_name}\n"
        f"URL: {url}\n\n"
        f"Website Text:\n{raw_content}\n\n"
        f"Generate the comprehensive executive brochure now."
    )

    if not client or not openai_api_key:
        return {
            "error": "OpenAI API key missing",
            "scraped_chars": len(raw_content),
            "brochure": "OpenAI API key is missing in your .env file."
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return {
            "error": None,
            "scraped_chars": len(raw_content),
            "brochure": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "error": str(e),
            "scraped_chars": len(raw_content),
            "brochure": f"Error generating brochure: {str(e)}"
        }


def stream_brochure_generator(company_name: str, url: str, model_choice: str) -> Generator[str, None, None]:
    """Streaming brochure generation for interactive Gradio UI (Lec 48)."""
    if not company_name.strip():
        yield "⚠️ Please enter a company name."
        return
    if not url.strip():
        yield "⚠️ Please enter a valid website URL."
        return

    yield f"🌐 **Step 1/2**: Scraping landing page from `{url}`..."
    content = scrape_website(url)

    if "[Scrape Error" in content:
        yield f"⚠️ Could not scrape `{url}`: {content}"
        return

    yield f"🧠 **Step 2/2**: Analyzing content with **{model_choice}** and drafting brochure...\n\n---\n"

    user_prompt = (
        f"Company Name: {company_name}\n"
        f"URL: {url}\n\n"
        f"Website Text:\n{content}\n\n"
        f"Generate the comprehensive executive brochure now."
    )

    accumulated = f"### 📄 Executive Brochure for {company_name}\n\n"

    if not client or not openai_api_key:
        yield "❌ OpenAI API key is missing in your .env file!"
        return

    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            accumulated += token
            yield accumulated
    except Exception as e:
        yield f"❌ Error: {str(e)}"


DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, expert AI Engineer mentor. "
    "Provide clear, encouraging, structured explanations using Markdown, bullet points, and code snippets when relevant."
)


def stream_llm(
    prompt: str,
    system_prompt: str,
    model_choice: str,
    temperature: float
) -> Generator[str, None, None]:
    """
    Calls LLM and yields tokens in real time using Python generators (`yield`).
    Gradio detects each yield and progressively updates the Markdown display (Lec 46 & 47).
    """
    if not prompt.strip():
        yield "⚠️ Please enter a prompt above to start streaming."
        return

    messages = [
        {"role": "system", "content": system_prompt or DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    accumulated = ""

    # Option A: Local Ollama
    if "Ollama" in model_choice:
        try:
            stream = ollama_client.chat.completions.create(
                model="llama3.2",
                messages=messages,
                temperature=temperature,
                stream=True
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                accumulated += token
                yield accumulated
            return
        except Exception as e:
            yield f"⚠️ Ollama error: {e}. Ensure `ollama serve` is running. Falling back to OpenAI."

    # Option B: OpenAI
    if not client or not openai_api_key:
        yield "❌ OpenAI API key is missing in your .env file! Please set `OPENAI_API_KEY`."
        return

    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            stream=True
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            accumulated += token
            yield accumulated
    except Exception as e:
        yield f"❌ Error: {str(e)}"


def create_gradio_app() -> gr.TabbedInterface:
    """Builds the complete 3-tab Gradio UI suite for direct mounting onto FastAPI (Lec 44–48)."""
    # Tab 1: Basics (Lec 44 & 45)
    tab1 = gr.Interface(
        fn=transform_text,
        inputs=[
            gr.Textbox(label="Your Input Text", placeholder="Type a sentence here...", lines=3),
            gr.Radio(
                choices=["SHOUT (Uppercase)", "whisper (lowercase)", "Reverse Text", "Word & Character Count"],
                value="SHOUT (Uppercase)",
                label="Transformation Style"
            )
        ],
        outputs=gr.Textbox(label="Transformed Output", lines=4, interactive=False),
        title="🚀 Gradio 101: Interactive UI Basics",
        flagging_mode="never"
    )

    # Tab 2: Real-Time LLM Token Streaming (Lec 46 & 47)
    with gr.Blocks() as tab2:
        gr.Markdown("### ⚡ Real-Time LLM Token Streaming (`yield` generator)")
        with gr.Row():
            with gr.Column(scale=1):
                stream_input = gr.Textbox(
                    label="Your Question / Prompt",
                    placeholder="e.g. Explain transformers using an intuitive analogy...",
                    lines=4
                )
                with gr.Accordion("⚙️ Model Parameters & Persona", open=False):
                    sys_input = gr.Textbox(label="System Prompt", value=DEFAULT_SYSTEM_PROMPT, lines=2)
                    model_drop = gr.Dropdown(
                        choices=["OpenAI (gpt-4o-mini)", "Local Ollama (llama3.2)"],
                        value="OpenAI (gpt-4o-mini)",
                        label="Model Engine"
                    )
                    temp_slide = gr.Slider(minimum=0.0, maximum=1.5, value=0.7, step=0.1, label="Temperature")
                
                stream_btn = gr.Button("🚀 Ask AI (Streaming)", variant="primary")
                stream_clear = gr.Button("🗑️ Clear")

            with gr.Column(scale=1):
                stream_output = gr.Markdown(label="AI Response", value="*The streamed response will type here live...*")

        stream_btn.click(
            fn=stream_llm,
            inputs=[stream_input, sys_input, model_drop, temp_slide],
            outputs=stream_output
        )
        stream_input.submit(
            fn=stream_llm,
            inputs=[stream_input, sys_input, model_drop, temp_slide],
            outputs=stream_output
        )
        stream_clear.click(lambda: ("", "*Cleared.*"), outputs=[stream_input, stream_output])

        gr.Examples(
            examples=[
                ["Explain the Transformer architecture to a layperson", DEFAULT_SYSTEM_PROMPT, "OpenAI (gpt-4o-mini)", 0.7],
                ["Explain the Transformer architecture to an aspiring AI engineer", DEFAULT_SYSTEM_PROMPT, "OpenAI (gpt-4o-mini)", 0.7],
                ["What is the key difference between RAG and Fine-tuning? Use a table.", DEFAULT_SYSTEM_PROMPT, "OpenAI (gpt-4o-mini)", 0.3],
                ["Write a Python function with type hints to calculate token latency.", DEFAULT_SYSTEM_PROMPT, "OpenAI (gpt-4o-mini)", 0.2]
            ],
            inputs=[stream_input, sys_input, model_drop, temp_slide]
        )

    # Tab 3: Brochure Generator (Lec 48)
    tab3 = gr.Interface(
        fn=stream_brochure_generator,
        inputs=[
            gr.Textbox(label="🏢 Company Name", placeholder="e.g. Hugging Face, Stripe, FastAPI"),
            gr.Textbox(label="🌐 Website URL", placeholder="e.g. https://huggingface.co"),
            gr.Dropdown(choices=["OpenAI (gpt-4o-mini)", "Local Ollama (llama3.2)"], value="OpenAI (gpt-4o-mini)", label="AI Engine")
        ],
        outputs=gr.Markdown(label="Generated Executive Brochure", value="*Brochure will stream live here...*"),
        title="🏢 AI Company Brochure Generator",
        examples=[
            ["Hugging Face", "https://huggingface.co", "OpenAI (gpt-4o-mini)"],
            ["FastAPI", "https://fastapi.tiangolo.com", "OpenAI (gpt-4o-mini)"],
            ["Ollama", "https://ollama.com", "OpenAI (gpt-4o-mini)"]
        ],
        flagging_mode="never"
    )

    return gr.TabbedInterface(
        interface_list=[tab1, tab2, tab3],
        tab_names=[
            "🚀 1. Gradio Basics (Lec 44-45)",
            "⚡ 2. LLM Streaming (Lec 46-47)",
            "🏢 3. Brochure Generator (Lec 48)"
        ],
        title="🎓 Week 2 • Day 2 — Gradio Web UI Master Suite (Lec 44–48)"
    )

