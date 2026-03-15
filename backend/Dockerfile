FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for librosa
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

EXPOSE 8000

# IMPORTANT: CMD must be "main:app" not "backend.main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
