import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph_agent import graph


st.set_page_config(page_title="Agent Chat")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = StreamlitChatMessageHistory(key="chat_messages")
    st.session_state.chat_history.add_message(
        SystemMessage("You are a helpful assistant.")
    )

# st.title("Agent Chat")

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
