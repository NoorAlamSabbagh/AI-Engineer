import os
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

# 2. Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Standard browser headers to avoid getting blocked by websites
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}


# ==========================================
# 1. Basic Single-Page Scraping & Summary
# ==========================================

def scrape_website_text(url: str) -> str:
    """Fetches a URL and strips away scripts, styles, and HTML tags."""
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove irrelevant tags
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
    body_text = soup.body.get_text(separator="\n", strip=True) if soup.body else ""

    # Keep first 3,000 characters
    combined = f"Title: {title}\n\nContent:\n{body_text}"
    return combined[:3000]


def generate_website_summary(scraped_content: str, tone: str) -> str:
    """Sends single-page scraped text to the LLM for summarization."""
    system_prompt = f"""
    You are an expert web content analyst.
    Your task is to summarize the provided website content.
    Style / Tone: {tone}.
    Use clean Markdown formatting with clear bullet points.
    """

    user_prompt = f"""
    Here is the content scraped from the website:
    ---
    {scraped_content}
    ---
    Provide a concise summary highlighting:
    1. What the organization/product does
    2. Key features, services, or offerings
    3. Any notable call to action or contact info
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# ==========================================
# 2. Multi-Page Brochure Generator Services
# ==========================================

def fetch_website_links(url: str) -> list[str]:
    """Scrapes all hyperlinks found on the given page and converts relative URLs to full URLs."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            # Convert relative links like '/about' into 'https://example.com/about'
            full_url = urljoin(url, href)
            if full_url.startswith("http"):
                links.append(full_url)
        return list(set(links))[:40]  # De-duplicate and cap to first 40 links
    except Exception:
        return []


def select_relevant_links(company_url: str, links: list[str]) -> list[dict]:
    """Uses LLM with Structured JSON output to select the best pages for a company brochure."""
    system_prompt = """
    You are an AI assistant that analyzes website links.
    Identify the most relevant links for creating an informative company brochure (e.g., About Us, Careers, Team, Products).
    Ignore irrelevant links like Privacy Policy, Terms, Login, or external social media.
    You MUST respond with valid JSON matching this schema:
    {
        "relevant_links": [
            {"type": "About Page", "url": "https://..."},
            {"type": "Careers Page", "url": "https://..."}
        ]
    }
    """

    user_prompt = f"Company URL: {company_url}\nAvailable Links:\n" + "\n".join(links)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},  # Guarantees valid JSON output!
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    try:
        data = json.loads(response.choices[0].message.content)
        return data.get("relevant_links", [])[:3]  # Limit to top 3 subpages to save speed & tokens
    except Exception:
        return []


def generate_brochure_markdown(company_name: str, combined_content: str) -> str:
    """Takes all gathered content from multiple pages and synthesizes a complete brochure."""
    system_prompt = """
    You are an expert corporate communications writer.
    Your task is to write a comprehensive, engaging brochure about a company for prospective customers, recruits, and partners.
    Format your response in clean Markdown with headers, bullet points, and key takeaways.
    """

    user_prompt = f"""
    Company Name: {company_name}
    
    Here is the information gathered from their website and key pages:
    ---
    {combined_content}
    ---
    
    Create a complete brochure covering:
    - Company Overview & Mission
    - Core Offerings & Solutions
    - Culture, Careers & Team (if found)
    - Why Choose Them / Unique Value
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content
