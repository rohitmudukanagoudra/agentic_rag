import sys
sys.path.append("./")
from llm.llm_setup import get_qa_chain

def vector_search(query: str, job_title: str, store):
    # Optionally combine job_title into the query
    full_query = f"{query} (Job Title: {job_title})"
    qa_chain = get_qa_chain(store)
    return qa_chain.invoke(full_query)