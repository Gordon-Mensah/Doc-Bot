import streamlit as st
from chat_tab import chat_tab
from jcoder_tab import jcoder_tab
from data_tab import data_tab

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
    # Pass model settings and live summary toggle
    chat_tab(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        use_live_search=use_live_search
    )

elif mode == "JCoder":
    # Pass model settings to JCoder
    jcoder_tab(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

elif mode == "Data Analyst":
    # Data tab is local-only for now; can be wired to the model later
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