import streamlit as st
import requests

# Helper function to query Ollama through ngrok
def query_ollama(prompt, model="llama3"):
    # Replace this with your actual ngrok URL from the terminal
    url = "https://abcd1234.ngrok.io/api/generate"
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
st.title("Doc-Bot (Cloud UI + Local Ollama)")

user_input = st.text_input("Ask Doc-Bot something:")
if st.button("Send"):
    answer = query_ollama(user_input)
    st.write(answer)
