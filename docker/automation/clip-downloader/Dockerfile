FROM python:3.12-alpine

# ffmpeg for video processing, build tools for yt-dlp
RUN apk add --no-cache ffmpeg ttf-freefont fontconfig && fc-cache -f

# Install Python deps
RUN pip install --no-cache-dir flask yt-dlp openai anthropic requests

WORKDIR /app
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
