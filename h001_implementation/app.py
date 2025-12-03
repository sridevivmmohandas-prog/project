import streamlit as st
from rag_pipeline import CustomerAgent

st.set_page_config(page_title="H-002 Agent", layout="wide")
st.title("🤖 H-002 Customer Support Agent")

if 'agent' not in st.session_state:
    st.session_state.agent = CustomerAgent()

if prompt := st.chat_input("Type: I'm cold"):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.agent.chat(prompt)
        st.write(response)
