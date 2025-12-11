import streamlit as st
from helpers import ollama_prompt, run_python_code
import matplotlib.pyplot as plt

def jcoder_tab(model="llama3.2", temperature=0.7, max_tokens=512):
    st.write("### 🖥️ JCoder Assistant")

    # Choose task
    task = st.radio("Choose what you want JCoder to do:",
                    ["Generate new code", "Explain code", "Adjust code", "Analyze code",
                     "Refactor code", "Run Python code", "OS Guidance"],
                    key="jcoder_radio_task")

    language = st.selectbox("Select language:",
                            ["Python", "JavaScript", "C++", "Java", "Rust", "Go", "Other"],
                            key="jcoder_select_language")

    # --- Generate ---
    if task == "Generate new code":
        desc = st.text_area("Describe the code you need:", height=150, key="jcoder_textarea_gen_desc")
        if st.button("Generate Code", key="jcoder_button_gen"):
            if desc.strip():
                prompt = f"Write {language} code for this request:\n{desc}"
                code = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write("### Generated Code")
                st.code(code, language=language.lower())
                st.session_state["last_code"] = code

    # --- Explain ---
    elif task == "Explain code":
        code_input = st.text_area("Paste your code here:", height=200, key="jcoder_textarea_explain")
        if st.button("Explain Code", key="jcoder_button_explain"):
            if code_input.strip():
                prompt = f"Explain this {language} code in simple terms:\n{code_input}"
                explanation = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write("### Explanation")
                st.write(explanation)
                st.session_state["last_code"] = code_input

    # --- Adjust ---
    elif task == "Adjust code":
        code_input = st.text_area("Paste your code here:", height=200, key="jcoder_textarea_adjust")
        adjustment = st.text_area("Describe how you want it adjusted:", height=100, key="jcoder_textarea_adjust_desc")
        if st.button("Adjust Code", key="jcoder_button_adjust"):
            if code_input.strip() and adjustment.strip():
                prompt = f"Here is some {language} code:\n{code_input}\n\nAdjust it as follows: {adjustment}"
                new_code = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write("### Adjusted Code")
                st.code(new_code, language=language.lower())
                st.session_state["last_code"] = new_code

    # --- Analyze ---
    elif task == "Analyze code":
        code_input = st.text_area("Paste your code here:", height=200, key="jcoder_textarea_analyze")
        if st.button("Analyze Code", key="jcoder_button_analyze"):
            if code_input.strip():
                prompt = f"Analyze this {language} code for bugs, style issues, and optimizations:\n{code_input}"
                analysis = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write("### Analysis")
                st.write(analysis)
                st.session_state["last_code"] = code_input

    # --- Refactor ---
    elif task == "Refactor code":
        code_input = st.text_area("Paste your code here:", height=200, key="jcoder_textarea_refactor")
        if st.button("Refactor Code", key="jcoder_button_refactor"):
            if code_input.strip():
                prompt = f"Refactor this {language} code to improve readability, efficiency, and structure:\n{code_input}"
                refactored = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write("### Refactored Code")
                st.code(refactored, language=language.lower())
                st.session_state["last_code"] = refactored

    # --- Run Python ---
    elif task == "Run Python code":
        code_input = st.text_area("Paste your Python code here:", height=200, key="jcoder_textarea_run")
        if st.button("Run Code", key="jcoder_button_run"):
            if code_input.strip():
                result, fig = run_python_code(code_input)
                st.write("### Output")
                st.code(result, language="text")
                if fig:
                    st.write("### Plot")
                    st.pyplot(fig)
                    plt.close(fig)
                st.session_state["last_code"] = code_input

    # --- OS Guidance ---
    elif task == "OS Guidance":
        os_choice = st.selectbox("Select your OS:", ["Windows", "macOS", "Linux"], key="jcoder_select_os")
        query = st.text_area("Describe what you need help with:", height=150, key="jcoder_textarea_os_query")
        if st.button("Get OS Guidance", key="jcoder_button_os"):
            if query.strip():
                prompt = f"Provide {os_choice}-specific instructions for this request:\n{query}"
                guidance = ollama_prompt(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write(f"### {os_choice} Guidance")
                st.write(guidance)
                st.session_state["last_code"] = guidance

    # --- Unified Follow-Up Box ---
    followup = st.chat_input("Ask a question or describe a change...")
    if followup and "last_code" in st.session_state:
        context = f"""Here is the current {language} code:
{st.session_state['last_code']}

User request:
{followup}

Respond with either an explanation or a modified version of the code, depending on what the user asked."""
        reply = ollama_prompt(context, model=model, temperature=temperature, max_tokens=max_tokens)
        with st.chat_message("assistant"):
            st.markdown(reply)
        if "```" in reply or reply.strip().startswith(language.lower()):
            st.session_state["last_code"] = reply
