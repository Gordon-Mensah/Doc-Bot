import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# -------------------------------
# Ollama via ngrok helper
# -------------------------------
def ollama_prompt_ngrok(prompt, model="llama3", temperature=0.7, max_tokens=512):
    # IMPORTANT: replace with your actual ngrok forwarding URL
    url = "https://blondish-tanklike-asia.ngrok-free.dev/api/generate"
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

def data_tab(model="llama3.2", temperature=0.7, max_tokens=512):
    st.write("### 📊 Data Analyst")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="data_tab_uploader")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # 🔧 Fix Arrow serialization issues: force object columns to string
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].astype(str)

            st.success("✅ File uploaded successfully!")
            st.write("### Preview of Data")
            st.dataframe(df.head())

            # Basic stats
            st.write("### Summary Statistics")
            st.write(df.describe(include="all"))

            # Visualization
            st.write("### Visualization")
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                x_axis = st.selectbox("Select X-axis column", numeric_cols, key="data_tab_x")
                y_axis = st.selectbox("Select Y-axis column", numeric_cols, key="data_tab_y")
                chart_type = st.radio("Choose chart type", ["Line", "Bar", "Scatter"], key="data_tab_chart")

                if st.button("Generate Chart", key="data_tab_button_chart"):
                    fig, ax = plt.subplots()
                    if chart_type == "Line":
                        ax.plot(df[x_axis], df[y_axis])
                    elif chart_type == "Bar":
                        ax.bar(df[x_axis], df[y_axis])
                    elif chart_type == "Scatter":
                        ax.scatter(df[x_axis], df[y_axis])
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)
                    ax.set_title(f"{chart_type} chart of {y_axis} vs {x_axis}")
                    st.pyplot(fig)
                    plt.close(fig)
            else:
                st.warning("No numeric columns available for visualization.")

            # Unified follow-up box with Ollama integration via ngrok
            followup = st.chat_input("Ask a question or describe a change...")
            if followup:
                # Convert a sample of the DataFrame to CSV string for context
                sample_csv = df.head(20).to_csv(index=False)
                context = f"""Here is a sample of the dataset (first 20 rows):

{sample_csv}

User request:
{followup}

Respond with either an explanation or a modified version of the code (e.g. pandas/matplotlib) that answers the question or performs the requested change."""
                reply = ollama_prompt_ngrok(context, model=model, temperature=temperature, max_tokens=max_tokens)
                with st.chat_message("assistant"):
                    st.markdown(reply)

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Upload a CSV file to begin analysis.")
