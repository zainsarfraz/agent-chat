import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph_agent import AgentGraph
from langgraph_agent import openai_llm as llm
from agent_tools import all_tools


if "chat_history" not in st.session_state:
    st.session_state.chat_history = StreamlitChatMessageHistory(key="chat_messages")
    st.session_state.chat_history.add_message(
        SystemMessage("You are a helpful assistant.")
    )

if "agent" not in st.session_state:
    st.session_state.agent = AgentGraph(llm=llm, tools=[])

if "selected_tools" not in st.session_state:
    st.session_state.selected_tools = []

st.subheader(f":robot_face: {st.session_state.agent.llm.model_name} Chatbot")

with st.sidebar:

    def tool_selected_on_change(*args):
        if args[0] not in st.session_state.selected_tools:
            st.session_state.selected_tools.append(args[0])
        else:
            st.session_state.selected_tools.remove(args[0])

    st.header("Select your tools here")
    for tool in all_tools:
        expander = st.expander(f"{tool.metadata['name']}", expanded=False)
        expander.toggle(
            tool.metadata["name"],
            False,
            on_change=tool_selected_on_change,
            args=(tool,),
        )
        expander.write(tool.metadata["display_text"])

    update_tools_button = st.button("Update Agent Tools", type="primary")
    if update_tools_button:
        del st.session_state.agent
        st.session_state.agent = AgentGraph(
            llm=llm, tools=st.session_state.selected_tools
        )


for message in st.session_state.chat_history.messages:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.add_user_message(user_input)

    status_progress_placeholder = st.container()

    graph = st.session_state.agent.graph

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response = ""
        for event in graph.stream(
            {"messages": st.session_state.chat_history.messages}, stream_mode="messages"
        ):
            if isinstance(event[0], ToolMessage):
                with status_progress_placeholder.status(
                    f"Executing tool {event[0].name}"
                ):
                    st.write(event[0])

            if isinstance(event[0], AIMessage):
                response += event[0].content
                response_placeholder.markdown(response)

    st.session_state.chat_history.add_ai_message(response)
