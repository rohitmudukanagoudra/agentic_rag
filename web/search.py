from langchain_community.tools.tavily_search import TavilySearchResults

web_search_tool = TavilySearchResults(k=10)

def web_search(query: str):
    return web_search_tool.run(query)
