FROM jauderho/yt-dlp:latest

RUN pip install --no-cache-dir flask

WORKDIR /app
COPY app.py .

EXPOSE 3030
CMD ["python", "app.py"]
