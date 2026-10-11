"""
Week 1 Web Scraper Utility
==========================
Fetches website content and cleans out scripts, styles, images, and inputs.
Works with any URL, handling standard HTTP headers and errors gracefully.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_website_contents(url: str, max_chars: int = 4000) -> str:
    """
    Fetches the website at `url`, strips non-content tags,
    and returns a clean text representation truncated to `max_chars`.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
        
        if soup.body:
            # Strip tags that do not contribute to readable content
            for tag in soup.body(["script", "style", "img", "input", "noscript", "svg"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
            
        full_content = f"Title: {title}\n\nContent:\n{text}"
        return full_content[:max_chars]
        
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

def fetch_website_links(url: str) -> list[str]:
    """
    Extracts all valid hyperlink URLs found on the given page.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://") or href.startswith("/"):
                links.append(href)
        return list(dict.fromkeys(links))  # remove duplicates while preserving order
    except Exception as e:
        print(f"Warning: Failed to fetch links from {url}: {e}")
        return []
