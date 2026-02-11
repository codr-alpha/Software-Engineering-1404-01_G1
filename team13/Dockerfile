FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies including zstd for Ollama
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config default-libmysqlclient-dev \
    ffmpeg \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh
RUN mkdir -p /root/.ollama/models

# Copy requirements
COPY requirements.txt /app/
COPY requirements.txt /app/team13-requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . /app/team13/
COPY templates/team13/ /app/templates/team13/
COPY static/team13/ /app/static/team13/

# Preload Whisper
RUN python -c "\
import whisper; \
print('🔄 Preloading Whisper model...'); \
whisper.load_model('base'); \
print('✅ Whisper model cached'); \
"

# Preload Ollama
RUN ollama serve & \
    sleep 5 && \
    ollama pull gemma3:4b && \
    pkill ollama || true

RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 3\n\
cd /app/team13 && \
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
gunicorn app404.wsgi:application -b 0.0.0.0:8000\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000
CMD ["/app/start.sh"]
