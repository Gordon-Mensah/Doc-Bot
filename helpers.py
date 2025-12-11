import requests
import urllib.parse
import io
import contextlib
import matplotlib.pyplot as plt

# ----------------------------
# Ollama Settings
# ----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"

# ----------------------------
# Ollama Prompt (single request)
# ----------------------------
def ollama_prompt(prompt, model=DEFAULT_MODEL, temperature=0.7, max_tokens=512):
    """
    Send a single prompt to Ollama and return the response.
    """
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            },
            timeout=300
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        return f"Error contacting Ollama: {e}"

# ----------------------------
# Ollama Chat (multi-turn)
# ----------------------------
def ollama_chat(messages, model=DEFAULT_MODEL, temperature=0.7, max_tokens=256):
    """
    Send chat history to Ollama. Messages should be a list of (role, text).
    """
    try:
        history_text = "\n".join([f"{role.upper()}: {msg}" for role, msg in messages])
        return ollama_prompt(history_text, model=model, temperature=temperature, max_tokens=max_tokens)
    except Exception as e:
        return f"Error in chat: {e}"

# ----------------------------
# Wikipedia Summary
# ----------------------------
def wikipedia_summary(query):
    """
    Fetch a summary from Wikipedia's REST API.
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote_plus(query)}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("extract", "No summary available.")
        return "Failed to fetch data."
    except Exception as e:
        return f"Error fetching Wikipedia data: {e}"

# ----------------------------
# Run Python Code Safely
# ----------------------------
def run_python_code(code: str):
    """
    Safely run Python code and capture stdout + plots.
    Returns (output_text, matplotlib_figure_or_None).
    """
    output_buffer = io.StringIO()
    fig = None
    try:
        with contextlib.redirect_stdout(output_buffer):
            local_env = {"plt": plt}
            exec(code, {}, local_env)
            if plt.get_fignums():
                fig = plt.gcf()
        return output_buffer.getvalue(), fig
    except Exception as e:
        return f"Error: {e}", None
