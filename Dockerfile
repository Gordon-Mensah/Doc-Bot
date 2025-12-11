# Base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

# Copy app code
COPY . /app

# Expose ports
EXPOSE 11434 10000

# Start Ollama in background and Streamlit in foreground
CMD ollama serve & streamlit run app.py --server.port=10000 --server.headless=true
