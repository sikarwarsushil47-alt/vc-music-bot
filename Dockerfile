FROM ghcr.io/pytgcalls/pytgcalls:latest

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir pyrogram tgcrypto yt-dlp

CMD ["python", "main.py"]
