from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from tools.tavily_tool import web_search
from tools.beautiful_soup import scrape_url
from rich import print
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import GoogleGenerativeAI





# LLM model
model = ChatMistralAI(model = "mistral-medium-2508")

# Search Agent --> search news, report etc. about the given topic
def search_Agent():
    return create_agent(
        model= model,
        tools= [web_search]
    )


# Reader Agent --> scrape the url and return clean and readable txt
def reader_Agent():
    return create_agent(
        model= model,
        tools= [scrape_url]
    )



# writer chain prompt 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}
    
    Research Gathered:
    {research}
    
    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)
    
    Be detailed, factual and professional.""")

])

writer_Chain = writer_prompt | model | StrOutputParser()



# Critic Chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    ...""")
])


critic_Chain = critic_prompt | model | StrOutputParser()