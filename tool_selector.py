import streamlit as st
from agent_tools import all_tools


def sidebar():
    with st.sidebar:
        st.header("Select your tools here")

        for tool in all_tools:
            expander = st.expander(f"{tool.metadata['name']}", expanded=True)
            tool_toggle = expander.toggle(tool.metadata["name"], True)
            if tool_toggle:
                pass
            expander.write(tool.metadata["display_text"])
