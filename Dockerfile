FROM python:3.12-slim

# Install system deps
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir yt-dlp fastapi uvicorn

WORKDIR /app
COPY app.py .

VOLUME ["/downloads"]

EXPOSE 3000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
