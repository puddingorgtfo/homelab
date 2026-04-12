FROM python:3.12-slim

# ffmpeg, fonts, curl/unzip for deno
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg fontconfig fonts-freefont-ttf curl unzip imagemagick \
    && fc-cache -f && rm -rf /var/lib/apt/lists/*

# Install Deno — required by yt-dlp 2026+ for YouTube n-challenge solving
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh

# Install Python deps (oauth2 plugin for YouTube TV client — bypasses PO token requirement)
RUN pip install --no-cache-dir flask yt-dlp yt-dlp-youtube-oauth2 openai anthropic requests playwright

# Install Chromium + system deps for Playwright (HTML → PNG card generation)
RUN playwright install chromium --with-deps

WORKDIR /app
COPY app.py .
COPY card_template.html .
COPY card_template_hook.html .
# Patched OAuth2 plugin: fixes device_code param name + HTTP 400 handling + player-only token filter
COPY youtubeoauth.py /usr/local/lib/python3.12/site-packages/yt_dlp_plugins/extractor/youtubeoauth.py

EXPOSE 5000
CMD ["python", "app.py"]
