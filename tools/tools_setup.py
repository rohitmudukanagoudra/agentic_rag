from langchain.tools import StructuredTool
from web.search import web_search
from vectorstore.search import vector_search

def get_tools(store):
    def vector_search_wrapper(query: str, job_title: str) -> str:
        return vector_search(query=query, job_title=job_title, store=store)

    return [
        StructuredTool.from_function(
            name="VectorStoreSearch",
            func=vector_search_wrapper,
            description="Search the vector store using a query and job title.",
            args_schema=None  # Optional, unless you want a custom schema
        ),
        StructuredTool.from_function(
            name="WebSearch",
            func=web_search,
            description="Use this to perform a web search for information."
        )
    ]
