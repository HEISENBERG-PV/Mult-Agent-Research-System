from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from tools.tavily_tool import web_search
from tools.beautiful_soup import scrape_url
from rich import print
# from langchain_google_genai import GoogleGenerativeAI


model = ChatMistralAI(model = "mistral-medium-2508")


search_Agent = create_agent(
    model= model,
    tools=[web_search],
    system_prompt="You are a helpful assistant which find the recent and reliable info from the internet"
)


while True:
    user_query = input("YOU : ")
    if user_query.lower == 'e':
        break

    result = search_Agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    }
    )      

    # print("AI : ", result['messages'][-1].content)
    print(result)


