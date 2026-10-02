from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
load_dotenv()

client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
MODEL = 'gpt-5-nano'
openai = OpenAI()

def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]

def get_links_user_prompt(url,links):
    user_prompt = f"""
        Here is the list of links on the website {url} -
        Please decide which of these are relevant web links for a brochure about the company, 
        respond with the full https URL in JSON format.
        Do not include Terms of Service, Privacy, email links.

        Links (some might be relative links):

        """
    user_prompt += "\n".join(links)
    return user_prompt


def select_relevant_links(link_system_prompt,user_prompt):
    response=client.responses.create(
        model=MODEL,
        input=[
            {"role": "developer", "content": link_system_prompt},
            {"role": "user", "content":user_prompt}
        ],
    )
    result = response.output_text
    links = json.loads(result)
    return links

def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]

def create_brochure_service(system_promt,user_prompt):
    response=client.responses.create(
    model=MODEL,
    input=[
        {"role": "developer", "content": system_promt},
        {"role": "user", "content":user_prompt}
    ],
    )
    result = response.output_text
    return result


def stream_brochure(system_prompt, user_prompt):

    stream = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "developer",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        stream=True
    )

    for event in stream:
        if event.type == "response.output_text.delta":
            yield event.delta

