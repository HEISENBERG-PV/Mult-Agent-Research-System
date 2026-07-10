from bs4 import BeautifulSoup
from langchain.tools import tool
import requests
import re


@tool
def scrape_url(url: str):
    "Scrape the url and return the clean and readable text "  #Docstring


    res = requests.get(                                         #Http req
        url=url,
        headers= {
            "User-Agent": "Mozilla/5.0"
        }
    )
    # print(res.text)

    soup = BeautifulSoup(res.text, "html.parser")               #Parsing html using Beautifulsoup
    # print(soup)

    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
        tag.decompose()
    
    text = soup.get_text(separator=" ", strip=True)[:3000]

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    
    return text

# print(scrape_url.invoke("https://aws.amazon.com/what-is/ai-automation"))
