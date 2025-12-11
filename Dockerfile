# Base image
FROM ubuntu:22.04

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (system service)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pre-pull models so they're ready when the container starts
RUN ollama pull llama3
RUN ollama pull llama3.2
RUN ollama pull mistral
RUN ollama pull qwen2
RUN ollama pull gemma

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose ports:
# - 11434 for Ollama (internal)
# - 10000 for Streamlit (Render will map $PORT)
EXPOSE 11434
EXPOSE 10000

# Start Ollama in the background, then run Streamlit on $PORT
CMD ollama serve & streamlit run app.py --server.port=$PORT --server.headless=true
