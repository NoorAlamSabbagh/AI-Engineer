"""
Week 1 Day 5 — Week 1 Capstone: Multi-Page Brochure Generator
============================================================
Crawls a company website, uses the LLM to identify relevant internal links,
scrapes the related pages, and synthesizes an executive company brochure.
"""

import os
import io
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_contents, fetch_website_links

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

def get_client_and_model():
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return OpenAI(api_key=key), "gpt-4o-mini", "OpenAI (Cloud)"
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "llama3.2", "Ollama (Local)"

def select_relevant_links(base_url: str, links: list[str], client, model: str) -> list[str]:
    """Uses LLM to filter the top 2-3 most informative links (About, Product, Mission)."""
    if not links:
        return []
        
    prompt = (
        f"Here are the hyperlinks found on '{base_url}':\n"
        f"{json.dumps(links[:20], indent=2)}\n\n"
        "Return a JSON array of the 2 most relevant links that would contain information "
        "about the company's background, products, or mission (e.g., /about, /company, /products). "
        "Return ONLY a valid JSON array of strings, e.g. [\"url1\", \"url2\"]."
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        raw = response.choices[0].message.content.strip()
        # Clean potential markdown fences
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        selected = json.loads(raw)
        return [l if l.startswith("http") else base_url.rstrip("/") + "/" + l.lstrip("/") for l in selected]
    except Exception:
        # Fallback heuristic
        return [l for l in links if any(k in l.lower() for k in ["about", "product", "company", "team"])][:2]

def generate_brochure(company_name: str, url: str) -> str:
    client, model_name, provider_label = get_client_and_model()
    print(f"🏢 Building brochure for '{company_name}' ({url}) via {provider_label}...")
    
    # 1. Scrape main landing page
    main_text = fetch_website_contents(url)
    
    # 2. Discover & select relevant subpages
    all_links = fetch_website_links(url)
    selected_subpages = select_relevant_links(url, all_links, client, model_name)
    print(f"🔗 Selected subpages: {selected_subpages}")

    # 3. Collect extra context
    subpage_contexts = []
    for sub_url in selected_subpages:
        sub_text = fetch_website_contents(sub_url, max_chars=2000)
        subpage_contexts.append(f"--- Subpage ({sub_url}) ---\n{sub_text}")
    
    combined_knowledge = f"{main_text}\n\n" + "\n\n".join(subpage_contexts)

    # 4. Synthesize brochure
    system_prompt = (
        "You are an elite corporate branding strategist. Create a professional, "
        "comprehensive company brochure in Markdown format based strictly on the provided materials.\n"
        "Include sections:\n"
        "1. Executive Overview & Mission\n"
        "2. Core Offerings / Products\n"
        "3. Key Strengths & Differentiators\n"
        "4. Contact & Next Steps"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Company Name: {company_name}\n\nWebsite Research:\n{combined_knowledge}"}
    ]

    print(f"✍️ Synthesizing brochure with {model_name}...")
    res = client.chat.completions.create(model=model_name, messages=messages, temperature=0.7)
    return res.choices[0].message.content.strip()

def run_day5_practice():
    print("=" * 60)
    print("🚀 Week 1 Day 5: Multi-Page Brochure Generator Capstone")
    print("=" * 60)
    
    brochure = generate_brochure("Edward Donner", "https://edwarddonner.com")
    print("\n📄 Generated Brochure:")
    print("=" * 60)
    print(brochure)
    print("=" * 60)
    print("\n🎉 Week 1 Day 5 completed!")

if __name__ == "__main__":
    run_day5_practice()
