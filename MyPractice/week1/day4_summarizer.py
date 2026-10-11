"""
Week 1 Day 4 — Website Scraper & Single-Page Summarizer
======================================================
Combines BeautifulSoup web scraping with an LLM prompt
to extract, clean, and summarize any web page.
"""

import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_contents

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

def get_client_and_model():
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return OpenAI(api_key=key), "gpt-4o-mini", "OpenAI (Cloud)"
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "llama3.2", "Ollama (Local)"

def summarize_website(url: str, tone: str = "snarky and witty") -> str:
    client, model_name, provider_label = get_client_and_model()
    print(f"🌐 Scraping website: {url} ...")
    content = fetch_website_contents(url)
    
    if content.startswith("Error fetching"):
        return content

    print(f"🤖 Generating {tone} summary using {provider_label} ({model_name})...\n")

    system_prompt = (
        f"You are a helpful, expert analyst. Analyze the provided website content "
        f"and write a concise summary in a {tone} tone. Use markdown bullet points."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is the website content to summarize:\n\n{content}"}
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def run_day4_practice():
    print("=" * 60)
    print("🚀 Week 1 Day 4: Single-Page Website Summarizer")
    print("=" * 60)
    
    test_url = "https://example.com"
    summary = summarize_website(test_url, tone="humorous and playful")
    
    print("📋 Generated Summary:")
    print("-" * 40)
    print(summary)
    print("-" * 40)
    print("\n🎉 Week 1 Day 4 completed!")

if __name__ == "__main__":
    run_day4_practice()
