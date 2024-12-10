from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from agent_tools import (
    google_search_tool,
    wikipedia_tool,
    youtube_search_tool,
    image_generation_tool,
    google_image_search_tool
)
from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

groq_api_key = os.environ["GROQ_API_KEY"]
model_name = "llama3-groq-70b-8192-tool-use-preview"
groq_llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name=model_name,
    streaming=True,
)

openai_api_key = os.environ["OPENAI_API_KEY"]
model_name = "gpt-4o-mini"
openai_llm = ChatOpenAI(api_key=openai_api_key, model=model_name, streaming=True)

tools = [google_search_tool, wikipedia_tool, youtube_search_tool, image_generation_tool, google_image_search_tool]

llm_with_tools = openai_llm.bind_tools(tools=tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
