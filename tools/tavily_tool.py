from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from tavily import TavilyClient
from rich import print
import requests
import json
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    "Search the web and fetch recent and reliable info about the topic given"
    result = tavily.search(
        query= query,
        max_results= 5
    )

    data = []

    for i in result["results"]:
        data.append(f"Title: {i['title']}\n URL: {i['url']}\n\n")

    return "".join(data)


# print(web_search.invoke("ai and automation"))