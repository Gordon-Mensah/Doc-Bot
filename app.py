import streamlit as st
import requests

# Function to query Ollama through ngrok tunnel
def query_ollama(prompt, model="llama3"):
    # Use your actual ngrok forwarding URL here
    url = "https://blondish-tanklike-asia.ngrok-free.dev/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Request failed: {e}"

# Streamlit UI
st.set_page_config(page_title="Doc-Bot", page_icon="🤖")
st.title("Doc-Bot (Streamlit Cloud + Local Ollama)")

st.write("Ask me anything — powered by Ollama running on your machine!")

user_input = st.text_area("Your question:", height=100)

if st.button("Send"):
    if user_input.strip():
        answer = query_ollama(user_input)
        st.markdown("### Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question before sending.")
