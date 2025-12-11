import streamlit as st
from helpers import ollama_chat, wikipedia_summary

def chat_tab(model="llama3.2", temperature=0.7, max_tokens=512, use_live_search=True):
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display past messages
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    # Input box for new message
    prompt = st.chat_input("Ask anything...")
    if prompt:
        # Show user message immediately
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        # Show placeholder while thinking
        with st.chat_message("assistant"):
            st.markdown("🧠 Thinking…")

        # Detect time-sensitive queries
        research_keywords = [
            "latest", "current", "today", "now", "update", "headline",
            "richest", "net worth", "price", "stock", "crypto", "breaking", "trending"
        ]
        is_time_sensitive = any(k in prompt.lower() for k in research_keywords)

        # Use Wikipedia for live summaries if enabled
        if use_live_search and is_time_sensitive:
            live_info = wikipedia_summary(prompt)
            if live_info and "No summary" not in live_info and "Failed" not in live_info:
                reply = f"📖 Wikipedia says:\n\n{live_info}\n\n(Always verify with trusted sources for the most current data.)"
            else:
                reply = ollama_chat(st.session_state.chat_history, model=model,
                                    temperature=temperature, max_tokens=max_tokens)
        else:
            reply = ollama_chat(st.session_state.chat_history, model=model,
                                temperature=temperature, max_tokens=max_tokens)

        # Save and display assistant reply
        st.session_state.chat_history.append(("assistant", reply))
        with st.chat_message("assistant"):
            st.markdown(reply)
