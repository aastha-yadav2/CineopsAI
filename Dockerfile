# Use official Python 3.10 slim image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and static web frontend
COPY src/ ./src/
COPY static/ ./static/

# Cloud Run default port & environment defaults
ENV PORT=8080 \
    CINEOPS_MOCK_MODE=1 \
    GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    GOOGLE_CLOUD_PROJECT=cineops-ai-507217 \
    GOOGLE_CLOUD_LOCATION=us-central1 \
    CINEOPS_GEMINI_MODEL=gemini-2.5-flash

# Expose target port
EXPOSE 8080

# Start Uvicorn bound to 0.0.0.0 and Cloud Run's dynamic $PORT
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT}"]
