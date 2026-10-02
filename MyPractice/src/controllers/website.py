import requests
from fastapi import HTTPException
from src.schemas.website import WebsiteSummarizeRequest, BrochureRequest
from src.services.website import (
    scrape_website_text,
    generate_website_summary,
    fetch_website_links,
    select_relevant_links,
    generate_brochure_markdown
)

def summarize_website_controller(request: WebsiteSummarizeRequest):
    try:
        # 1. Scrape the website content
        content = scrape_website_text(request.url)
        
        # 2. Feed scraped text into the LLM
        summary = generate_website_summary(content, request.tone)
        
        return {
            "status": "success",
            "url": request.url,
            "tone": request.tone,
            "summary": summary
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch website: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Summarization error: {str(e)}")



def create_brochure_controller(request: BrochureRequest):
    try:
        # Step A: Scrape Landing Page
        landing_page_content = scrape_website_text(request.url)
        all_gathered_content = f"### Landing Page Content:\n{landing_page_content}\n\n"
        # Step B: Discover Sub-links
        all_links = fetch_website_links(request.url)
        # Step C: Let LLM pick the 2-3 most relevant pages
        relevant_links = select_relevant_links(request.url, all_links)
        # Step D: Scrape each relevant subpage
        scraped_sources = [{"page": "Homepage", "url": request.url}]
        for item in relevant_links:
            page_type = item.get("type", "Subpage")
            sub_url = item.get("url")
            if sub_url and sub_url != request.url:
                try:
                    subpage_text = scrape_website_text(sub_url)
                    all_gathered_content += f"### {page_type} ({sub_url}):\n{subpage_text}\n\n"
                    scraped_sources.append({"page": page_type, "url": sub_url})
                except Exception:
                    continue
        # Step E: Synthesize into final Markdown brochure
        brochure = generate_brochure_markdown(request.company_name, all_gathered_content[:8000])
        return {
            "status": "success",
            "company_name": request.company_name,
            "sources_analyzed": scraped_sources,
            "brochure": brochure
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brochure creation failed: {str(e)}")