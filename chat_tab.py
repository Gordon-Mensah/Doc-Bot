import streamlit as st
import requests
from helpers import wikipedia_summary

# -------------------------------
# Ollama helper (no ngrok)
# -------------------------------
def ollama_chat_local(chat_history, model="llama3", temperature=0.7, max_tokens=512):
    # Ollama runs locally inside the Render container
    url = "http://localhost:11434/api/generate"
    # Build prompt from chat history
    prompt = "\n".join([f"{role}: {msg}" for role, msg in chat_history])
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Request failed: {e}"

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
                # Call Ollama locally
                reply = ollama_chat_local(
                    st.session_state.chat_history,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
        else:
            # Call Ollama locally
            reply = ollama_chat_local(
                st.session_state.chat_history,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

        # Save and display assistant reply
        st.session_state.chat_history.append(("assistant", reply))
        with st.chat_message("assistant"):
            st.markdown(reply)
