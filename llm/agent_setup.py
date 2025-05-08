# from langchain.agents.output_parsers import JSONAgentOutputParser
# from langchain.agents.format_scratchpad import format_log_to_str
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.agents import AgentExecutor


# def create_agent(prompt, tools, llm):
#     chain = (
#         RunnablePassthrough.assign(
#             agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
#         )
#         | prompt
#         | llm
#         | JSONAgentOutputParser()
#     )

#     agent_executor = AgentExecutor(
#         agent=chain,
#         tools=tools,
#         handle_parsing_errors=True,
#         max_iterations=5,
#         verbose=True
#     )
#     return agent_executor


from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel

def create_agent(prompt: ChatPromptTemplate, tools: list[StructuredTool], llm: BaseChatModel):
    agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        max_iterations=5,
        verbose=True
    )
    return agent_executor
