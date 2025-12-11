import streamlit as st
import requests
from chat_tab import chat_tab
from jcoder_tab import jcoder_tab
from data_tab import data_tab

# -------------------------------
# Ollama via ngrok helper
# -------------------------------
def query_ollama(prompt, model="llama3", temperature=0.7, max_tokens=512):
    # IMPORTANT: replace with your actual ngrok forwarding URL
    url = "https://YOUR-NGROK-URL.ngrok-free.dev/api/generate"
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
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Request failed: {e}"

# -------------------------------
# App config
# -------------------------------
st.set_page_config(
    page_title="Fast Local AI",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------
# Sidebar – Navigation & Settings
# -------------------------------
st.sidebar.title("⚡ Fast Local AI")
mode = st.sidebar.radio(
    "Navigation",
    ["Chat", "JCoder", "Data Analyst"],
    key="sidebar_radio_mode"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Model settings")

# Model selection
model = st.sidebar.selectbox(
    "Model",
    ["llama3.2", "llama3", "mistral", "qwen2", "gemma"],
    index=0,
    key="sidebar_select_model"
)

# Generation controls
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.70,
    step=0.05,
    key="sidebar_slider_temperature"
)

max_tokens = st.sidebar.number_input(
    "Max tokens",
    min_value=64,
    max_value=4096,
    value=512,
    step=64,
    key="sidebar_number_max_tokens"
)

# Optional live summaries (for Chat tab)
use_live_search = st.sidebar.toggle(
    "Enable Wikipedia live summaries",
    value=False,
    key="sidebar_toggle_live_search"
)

st.sidebar.markdown("---")
st.sidebar.caption("Built for speed, clarity, and iteration.")

# -------------------------------
# Session state defaults
# -------------------------------
if "last_code" not in st.session_state:
    st.session_state["last_code"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# -------------------------------
# Header
# -------------------------------
st.title("Fast Local AI")
st.write("A clean, focused assistant for coding, conversation, and data analysis.")

# -------------------------------
# Mode routing
# -------------------------------
if mode == "Chat":
    chat_tab(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        use_live_search=use_live_search,
        query_fn=query_ollama  # pass ngrok/Ollama function
    )

elif mode == "JCoder":
    jcoder_tab(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        query_fn=query_ollama  # pass ngrok/Ollama function
    )

elif mode == "Data Analyst":
    data_tab()

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("⚡ Fast Local AI — built for speed, clarity, and iteration.")
    st.caption("Chat: freeform Q&A with optional live summaries.")

with col2:
    st.caption("JCoder: Generate, explain, adjust, analyze, refactor, run Python, and get OS guidance.")
    st.caption("Data Analyst: Upload CSVs, preview, summarize, and visualize your datasets.")

with col3:
    st.caption("Made with Streamlit + Ollama integration.")
    st.caption("For privacy details, see: https://privacy.microsoft.com/en-us/privacystatement")
    st.caption("© 2024 Fast Local AI")
    st.caption("All rights reserved.")
