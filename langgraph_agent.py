from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from agent_tools import all_tools
from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]
model_name = "llama-3.2-90b-vision-preview"
groq_llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name=model_name,
    streaming=True,
)

openai_api_key = os.environ["OPENAI_API_KEY"]
model_name = "gpt-4o-mini"
openai_llm = ChatOpenAI(api_key=openai_api_key, model=model_name, streaming=True)

class State(TypedDict):
    messages: Annotated[list, add_messages]


class AgentGraph():
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(tools=tools)
        else:
            self.llm_with_tools = self.llm
        self.graph_builder = StateGraph(State)
        self.graph = None
        self.build_graph()

    def chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}


    def build_graph(self):
        self.graph_builder.add_node("chatbot", self.chatbot)
        self.graph_builder.add_edge(START, "chatbot")
        if self.tools:
            tool_node = ToolNode(tools=self.tools)
            self.graph_builder.add_node("tools", tool_node)
            self.graph_builder.add_conditional_edges(
                "chatbot",
                tools_condition,
            )
            self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        self.graph = self.graph_builder.compile()
        print(f"Graph build with {len(self.tools)} tools")
