from agents import build_reader_Agent, build_search_Agent, writer_Chain, critic_Chain
from rich import print

def research_pipeline(topic : str) -> dict:

    state = {}


    print('Step 1: searching recent news from internet')

    # SEARCH AGENT
    search_Agent = build_search_Agent()
    search_agent_result = search_Agent.invoke({
        'messages': [('user', f'find recent, reliable and detailed information about the {topic}')]
    })

    # print("SEARCH AGENT RESULT \n", search_agent_result)
    # print("*"*200)

    state['search_agent_result'] = search_agent_result['messages'][-1].content

    print("\n search result ",state['search_agent_result'])

    print("Step 2 : Scraping the top resources ")
    # READER AGENT 
    reader_Agent = build_reader_Agent()
    reader_agent_result = reader_Agent.invoke({
         "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_agent_result'][:800]}"
        )]
    })
    # print('READER AGENT RESULT \n', reader_agent_result)
    # print("*"*200)
    state['scraped_content'] = reader_agent_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    combined_research = {
        f"SEARCH RESULT : {state['search_agent_result']}",
        f"SCRAPED CONTENT : {state['scraped_content']}"
    }


    # WRITER CHAIN

    print("Step 3 : Drafting the final report ")
    state['report'] = writer_Chain.invoke({
        'topic': topic,
        'research': combined_research
    })

    print("\n Final Report\n",state['report'])

    # CRITIC CHAIN

    print("Step 4 : Crtic is reviewing the report")
    state['feedback'] = critic_Chain.invoke({
        'report': state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    research_pipeline(topic)