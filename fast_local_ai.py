# fast_local_ai.py
import streamlit as st
import requests

st.set_page_config(page_title="Fast Local AI", page_icon="⚡")
st.title("⚡ Fast Local AI (Ollama-powered)")

# Sidebar settings
model = st.sidebar.selectbox("Model", ["llama3.2", "mistral", "phi3", "qwen:0.5b"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
max_tokens = st.sidebar.slider("Max tokens", 64, 1024, 256)

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

# Input
prompt = st.chat_input("Ask your AI anything...")
if prompt:
    st.session_state.history.append(("user", prompt))

    # Build prompt from history
    history_text = "\n".join([f"{r.upper()}: {m}" for r, m in st.session_state.history])

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": history_text,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "stream": False
                    },
                    timeout=120,
                )
                reply = response.json().get("response", "").strip()
            except Exception as e:
                reply = f"Error: {e}"

        st.markdown(reply)
        st.session_state.history.append(("assistant", reply))
