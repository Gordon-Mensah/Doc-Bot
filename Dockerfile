FROM ubuntu:22.04

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose ports
EXPOSE 11434
EXPOSE 10000

# Start Ollama, pull models, then run Streamlit
CMD ollama serve & \
    sleep 5 && \
    ollama pull llama3 || true && \
    ollama pull llama3.2 || true && \
    ollama pull mistral || true && \
    ollama pull qwen2 || true && \
    ollama pull gemma || true && \
    streamlit run app.py --server.port=$PORT --server.headless=true
