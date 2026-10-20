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


def create_gradio_app() -> gr.TabbedInterface:
    """Builds the 3-tab Gradio UI suite for direct mounting onto FastAPI (Lec 44–48)."""
    # Tab 1: Basics
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

    # Tab 2: Brochure Generator
    tab2 = gr.Interface(
        fn=stream_brochure_generator,
        inputs=[
            gr.Textbox(label="🏢 Company Name", placeholder="e.g. Hugging Face, Stripe, FastAPI"),
            gr.Textbox(label="🌐 Website URL", placeholder="e.g. https://huggingface.co"),
            gr.Dropdown(choices=["OpenAI (gpt-4o-mini)", "Local Ollama (llama3.2)"], value="OpenAI (gpt-4o-mini)", label="AI Engine")
        ],
        outputs=gr.Markdown(label="Generated Executive Brochure", value="*Brochure will stream live here...*"),
        title="🏢 AI Company Brochure Generator",
        flagging_mode="never"
    )

    return gr.TabbedInterface(
        interface_list=[tab1, tab2],
        tab_names=["🚀 1. Gradio Basics (Lec 44-45)", "🏢 2. Brochure Generator (Lec 48)"],
        title="🎓 Week 2 • Day 2 — Gradio Web UI Master Suite"
    )
