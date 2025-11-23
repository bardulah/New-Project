FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p psyche_edge/data/biometrics \
    psyche_edge/data/decisions \
    psyche_edge/data/agent_logs \
    psyche_edge/data/evolution_history

# Expose Streamlit port
EXPOSE 8501

# Expose Telegram bot port (if needed)
EXPOSE 8080

# Default command - run Streamlit
CMD ["streamlit", "run", "psyche_edge/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
