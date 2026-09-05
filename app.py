import streamlit as st
from agent import ask_agent
import database

# --- Initialize database once ---
database.init_db()

# --- Page setup ---
st.set_page_config(page_title="AI Task Agent", page_icon="🤖")
st.title("🤖 AI Task Agent")
st.caption("Powered by Google's Gemini API — built with Python & Streamlit")

with st.sidebar:
    st.header("About")
    st.write(
        "This is an AI task management agent built from scratch using the "
        "Gemini API. It can understand natural language, extract tasks, "
        "save them permanently, and reason over your task list to answer "
        "questions like 'what are my urgent tasks?'"
    )
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# --- Session state setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display past messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Handle new user input ---
user_input = st.chat_input("Ask me anything, or tell me what you need to do...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply_text = ask_agent(user_input)
            except Exception as e:
                reply_text = f"Something went wrong: {e}"

            st.write(reply_text)

    st.session_state.messages.append({"role": "assistant", "content": reply_text})