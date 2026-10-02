from app.services.website import (
    fetch_website_links,
    get_links_user_prompt,
    select_relevant_links,
    fetch_website_contents,
    create_brochure_service,
    stream_brochure
)
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.website import Create_Brochure_Request


def create_brochure(request: Create_Brochure_Request):
    try:
        link_system_prompt = """
            You are provided with a list of links found on a webpage.
           You are able to decide which of the links would be most relevant to include in a brochure about the company,
            such as links to an About page, or a Company page, or Careers/Jobs pages.
            You should respond in JSON as in this example:

            {
                "links": [
                    {"type": "about page", "url": "https://full.url/goes/here/about"},
                    {"type": "careers page", "url": "https://another.full.url/careers"}
                ]
            }
            """
        links = fetch_website_links(request.url)
        user_prompt = get_links_user_prompt(request.url, links)
        relevant_links = select_relevant_links(link_system_prompt, user_prompt)

        contents = fetch_website_contents(request.url)
        result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
        for link in relevant_links["links"]:
            result += f"\n\n### Link: {link['type']}\n"
            result += fetch_website_contents(link["url"])

        brochure_system_prompt = """
            You are an assistant that analyzes the contents of several relevant pages from a company website
            and creates a short brochure about the company for prospective customers, investors and recruits.
            Respond in markdown without code blocks.
            Include details of company culture, customers and careers/jobs if you have the information.
            """

        user_prompt = f"""
            You are looking at a company called: {request.company_name}
            Here are the contents of its landing page and other relevant pages;
            use this information to build a short brochure of the company in markdown without code blocks.\n\n
            """
        user_prompt += result
        user_prompt = user_prompt[:5_000]

        return StreamingResponse(
            stream_brochure(brochure_system_prompt, user_prompt), media_type="text/plain"
        )
        brochure = create_brochure_service(brochure_system_prompt, user_prompt)

        return brochure
        # return fetch_website_links("https://edwarddonner.com")
        return fetch_website_links(request.url)
    except Exception as error:
        print(f"Error while create brochure  : {error}")
        raise HTTPException(status_code=500, detail="Failed to create brochure")
