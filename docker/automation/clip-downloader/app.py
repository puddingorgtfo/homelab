import os
import json
import subprocess
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_OUTPUT_DIR = '/mnt/nas/n8n/content-images'
PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL', 'https://media.burnhamandsons.com')


def _extract_video_id(url):
    """Extract YouTube video ID from any URL format. Returns the full URL if not recognized."""
    if not url:
        return ''
    import re
    # youtube.com/watch?v=ID, youtube.com/shorts/ID, youtu.be/ID, youtube.com/embed/ID
    m = re.search(r'(?:v=|/shorts/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})', url)
    return m.group(1) if m else url


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


def _do_download(query, niche_slug, date, index, max_duration, excluded_urls=None):
    """Core clip download logic. Returns a result dict."""
    excluded_urls = {_extract_video_id(u) for u in (excluded_urls or []) if u}
    if not query:
        return {'success': False, 'error': 'query is required', 'index': index}

    import time as _time
    output_dir = os.path.join(BASE_OUTPUT_DIR, date)
    os.makedirs(output_dir, exist_ok=True)
    epoch = int(_time.time())
    filename = f'{niche_slug}-{date}-{index}-{epoch}.mp4'
    output_path = os.path.join(output_dir, filename)

    tmp_dir = tempfile.mkdtemp()
    tmp_output = os.path.join(tmp_dir, 'raw.%(ext)s')

    try:
        download_duration = max_duration + 30

        def _run_yt(search_q, use_duration_filter, timeout_s):
            """Run yt-dlp and return (result, source_title, source_url, source_duration, raw_file)."""
            cmd = [
                'yt-dlp',
                '--no-playlist',
                '--username', 'oauth2', '--password', '',
                '--remote-components', 'ejs:github',
                '--format', 'best[height<=720]/best[height<=480]/worst[ext=mp4]/worst',
                '--download-sections', f'*0:00-{download_duration}',
                '--print', 'before_dl:%(title)s|||%(webpage_url)s|||%(duration)s',
                '-o', tmp_output,
            ]
            if use_duration_filter:
                cmd += ['--match-filter', 'duration<600']
            cmd.append(search_q)
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=tmp_dir)
            s_title, s_url, s_dur = '', '', 0
            for line in res.stdout.splitlines():
                if '|||' in line:
                    parts = line.split('|||')
                    s_title = parts[0].strip() if len(parts) > 0 else ''
                    s_url   = parts[1].strip() if len(parts) > 1 else ''
                    try:
                        s_dur = float(parts[2].strip()) if len(parts) > 2 else 0
                    except (ValueError, TypeError):
                        s_dur = 0
                    # no break — keep iterating so the LAST match wins
                    # (yt-dlp may print before_dl for multiple candidates; the last one is the actual download)
            r_file = None
            for f in os.listdir(tmp_dir):
                if f.startswith('raw.') and not f.endswith('.part'):
                    r_file = os.path.join(tmp_dir, f)
                    break
            # Extra safety: if source is a full episode despite filter, reject it
            if r_file and s_dur > 600:
                os.remove(r_file)
                r_file = None
            return res, s_title, s_url, s_dur, r_file

        source_title, source_url = '', ''

        # Primary: ytsearch3 with duration filter (<10 min) — avoids full podcast episodes
        _, source_title, source_url, _, raw_file = _run_yt(
            f'ytsearch3:{query}', use_duration_filter=True, timeout_s=90
        )
        if raw_file and not _title_matches_query(source_title, query):
            os.remove(raw_file)
            raw_file = None
        if raw_file and _extract_video_id(source_url) in excluded_urls:
            os.remove(raw_file)
            raw_file = None

        # Fallback 1: append "podcast clip" and try 5 results, no hard duration filter
        # (match-filter already applied above; fallback is more permissive to find anything)
        if not raw_file:
            _, source_title, source_url, _, raw_file = _run_yt(
                f'ytsearch5:{query} podcast clip', use_duration_filter=False, timeout_s=90
            )
            if raw_file and not _title_matches_query(source_title, query):
                os.remove(raw_file)
                raw_file = None
            if raw_file and _extract_video_id(source_url) in excluded_urls:
                os.remove(raw_file)
                raw_file = None

        # Fallback 2: simplified query (first 6 words), no duration check at all.
        # The full combined query (youtube_search_query + suffix) can be 10+ words —
        # too specific for YouTube to return any results. Truncating to 6 words gives
        # a broader search that almost always finds something. ffmpeg -t still trims to
        # max_duration regardless of source video length.
        if not raw_file:
            def _run_yt_any(search_q, timeout_s, max_duration_s=None):
                """Like _run_yt but with optional duration cap (default: no limit)."""
                cmd = [
                    'yt-dlp',
                    '--no-playlist',
                    '--username', 'oauth2', '--password', '',
                    '--remote-components', 'ejs:github',
                    '--format', 'best[height<=720]/best[height<=480]/worst[ext=mp4]/worst',
                    '--download-sections', f'*0:00-{download_duration}',
                    '--print', 'before_dl:%(title)s|||%(webpage_url)s|||%(duration)s',
                    '-o', tmp_output,
                ]
                if max_duration_s:
                    cmd += ['--match-filter', f'duration<{max_duration_s}']
                cmd.append(search_q)
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=tmp_dir)
                s_title, s_url = '', ''
                for line in res.stdout.splitlines():
                    if '|||' in line:
                        parts = line.split('|||')
                        s_title = parts[0].strip() if len(parts) > 0 else ''
                        s_url   = parts[1].strip() if len(parts) > 1 else ''
                        # no break — last match wins (actual downloaded video)
                r_file = None
                for f in os.listdir(tmp_dir):
                    if f.startswith('raw.') and not f.endswith('.part'):
                        r_file = os.path.join(tmp_dir, f)
                        break
                return s_title, s_url, r_file

            # Fallback 2: first 5 words + "podcast clip shorts" + 5-min cap.
            short_q = ' '.join(query.split()[:5]) + ' podcast clip shorts'
            source_title, source_url, raw_file = _run_yt_any(
                f'ytsearch1:{short_q}', timeout_s=60, max_duration_s=300
            )
            if raw_file and not _title_matches_query(source_title, query, min_matches=1):
                os.remove(raw_file)
                raw_file = None
            if raw_file and _extract_video_id(source_url) in excluded_urls:
                os.remove(raw_file)
                raw_file = None

        # Fallback 3 (last resort): first 2 words (speaker name) + "podcast" — no title
        # check, no duration filter. Guarantees something comes back so the queue row
        # always has a video, even if it's not the ideal clip.
        if not raw_file:
            speaker_q = ' '.join(query.split()[:2]) + ' podcast'
            source_title, source_url, raw_file = _run_yt_any(
                f'ytsearch1:{speaker_q}', timeout_s=45
            )
            if raw_file and _extract_video_id(source_url) in excluded_urls:
                os.remove(raw_file)
                raw_file = None

        if not raw_file or not os.path.exists(raw_file):
            return {
                'success': False,
                'error': 'No suitable clip found after all fallbacks.',
                'index': index
            }

        # Encode to local tmp first (NFS doesn't support seeks needed by +faststart)
        tmp_encoded = os.path.join(tmp_dir, 'encoded.mp4')

        # Blurred background + letterboxed foreground — preserves full horizontal content.
        # Background: scale to overfill 1080x1920, crop, blur.
        # Foreground: scale to fit within 1080x1920 (shows full width, bars top/bottom).
        blur_filter = (
            '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,'
            'crop=1080:1920,gblur=sigma=20[bg];'
            '[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];'
            '[bg][fg]overlay=0:(H-h)/2[out]'
        )
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', raw_file,
            '-filter_complex', blur_filter,
            '-map', '[out]', '-map', '0:a',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-t', str(download_duration),
            tmp_encoded
        ]

        # Use Popen+DEVNULL to avoid capture_output pipe deadlock on timeout
        with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as proc:
            try:
                proc.wait(timeout=300)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return {'success': False, 'error': 'Download timed out (>4 min).', 'index': index}
        encode_ok = (proc.returncode == 0 and os.path.exists(tmp_encoded))

        if not encode_ok:
            ffmpeg_cmd_simple = [
                'ffmpeg', '-y',
                '-i', raw_file,
                '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',
                '-t', str(download_duration),
                tmp_encoded
            ]
            with subprocess.Popen(ffmpeg_cmd_simple, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as proc2:
                try:
                    proc2.wait(timeout=300)
                except subprocess.TimeoutExpired:
                    proc2.kill()
                    proc2.wait()
                    return {'success': False, 'error': 'Download timed out (>4 min).', 'index': index}
            if proc2.returncode != 0 or not os.path.exists(tmp_encoded):
                return {
                    'success': False,
                    'error': 'ffmpeg encoding failed',
                    'index': index
                }

        # Enhance with captions + optional storyboard overlay, then copy to NAS
        enhanced, clip_transcript = _enhance_clip(tmp_encoded, tmp_dir, query, max_duration)
        shutil.copy2(enhanced, output_path)

        public_url = f'{PUBLIC_BASE_URL}/{date}/{filename}'

        return {
            'success': True,
            'filename': filename,
            'public_url': public_url,
            'source_title': source_title,
            'source_url': source_url,
            'clip_transcript': clip_transcript,
            'output_path': output_path,
            'index': index,
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Download timed out (>4 min).',
            'index': index
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'index': index
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _find_natural_cutoff(words, max_duration, min_fraction=0.75):
    """
    Find the last natural speech boundary at or before max_duration.
    Prefers sentence-ending punctuation or long pauses (>= 0.8s gap to next word).
    Falls back to max_duration so we never cut a clip short unnecessarily.
    min_fraction: don't cut earlier than max_duration * this (avoids cutting before the payoff).
    """
    if not words:
        return max_duration

    min_time = max_duration * min_fraction
    best = None

    for i, w in enumerate(words):
        if w['end'] > max_duration:
            break
        if w['end'] < min_time:
            continue

        word_text = w['word'].strip()
        is_sentence_end = any(word_text.endswith(p) for p in ('.', '!', '?'))

        # Only measure gap when there's a next word — end-of-list is not a pause
        if i + 1 < len(words):
            gap = words[i + 1]['start'] - w['end']
            is_long_pause = gap >= 0.8
        else:
            is_long_pause = False

        if is_sentence_end or is_long_pause:
            best = w['end'] + 0.15  # small tail buffer after the word

    if best is not None:
        return min(best, max_duration)

    # No natural boundary found — use full max_duration rather than cutting short
    return max_duration


def _title_matches_query(title, query, min_matches=1):
    """
    Return True if the video title contains at least min_matches significant keywords
    from the search query (words longer than 3 chars). Prevents grabbing completely
    off-topic videos (e.g. commencement speeches when searching for podcast clips).
    If there aren't enough keywords to meet min_matches, always returns True.
    """
    keywords = {w.lower().strip('.,!?"\'') for w in query.split() if len(w) > 3}
    if len(keywords) < min_matches:
        return True  # not enough keywords to be strict
    title_lower = title.lower()
    matches = sum(1 for kw in keywords if kw in title_lower)
    return matches >= min_matches


def _find_hook_start(words, full_text, context_hint='', max_duration=60):
    """
    Use Claude Haiku to find where the 'hook' starts in a podcast transcript.
    Analyzes the first ~30s of speech to identify intro vs. compelling content.
    Returns hook_start_time (float seconds). Falls back to 0.0 on any failure.
    """
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not anthropic_key:
        return 0.0

    # Too short to have a meaningful intro
    if len(words) < 15:
        return 0.0

    # Only send the first ~30s of transcript to Claude (intros are at the start)
    analysis_window = min(30.0, max_duration)
    window_words = [w for w in words if w['start'] < analysis_window]
    if len(window_words) < 10:
        return 0.0

    # Format transcript with timestamps for precise hook identification
    formatted = ' '.join(f"[{w['start']:.2f}] {w['word']}" for w in window_words)

    prompt = (
        'You analyze podcast clip transcripts to find where the "hook" starts — '
        'the moment that would grab a viewer\'s attention on social media.\n\n'
        f'CONTEXT: This clip was found by searching YouTube for: "{context_hint}"\n\n'
        f'Transcript with word-level timestamps:\n{formatted}\n\n'
        'Your job: Find the FIRST timestamp where the clip should START to maximize '
        'viewer retention on social media (TikTok, Instagram Reels, YouTube Shorts).\n\n'
        'SKIP these intro patterns — they bore viewers:\n'
        '- Theme music / jingles (silence or music before speech)\n'
        '- "Welcome back to the show" / "Hey guys" / "What\'s up everybody"\n'
        '- Sponsor reads / "This episode is brought to you by..."\n'
        '- Generic setup: "So today we\'re going to talk about..." / "I\'ve been thinking about..."\n'
        '- Host introductions: "I\'m here with..." / "My guest today is..."\n'
        '- Podcast name drops: "This is The XYZ Podcast"\n\n'
        'KEEP — do NOT skip these even if they come early:\n'
        '- Any statement or question that provides CONTEXT needed to understand what follows\n'
        '  (e.g. "When I was deployed in Afghanistan..." sets up a war story — keep it)\n'
        '- A provocative claim, controversial opinion, or surprising fact\n'
        '- An emotional moment (anger, laughter, shock, vulnerability)\n'
        '- A direct question that hooks curiosity ("Do you know what happens when...")\n'
        '- Story setup that is already compelling ("I got a call at 3 AM...")\n\n'
        'RULES:\n'
        '1. The hook must start at a COMPLETE THOUGHT — never mid-sentence or mid-idea\n'
        '2. A viewer seeing this clip with ZERO prior context must understand what\'s being said\n'
        '3. If the clip has NO intro (content starts immediately), return 0.0\n'
        '4. If you\'re unsure, be conservative — start earlier rather than later\n'
        '5. Never skip more than 50% of the transcript — that means the whole clip is intro\n\n'
        'Return ONLY this JSON (no markdown, no explanation):\n'
        '{"hook_start": <float seconds>, "reason": "<one sentence why this is the hook>"}'
    )

    try:
        from anthropic import Anthropic
        ac = Anthropic(api_key=anthropic_key)
        resp = ac.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=150,
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw = resp.content[0].text.strip()
        # Strip markdown code fences if Claude wrapped the JSON
        if raw.startswith('```'):
            raw = raw.split('\n', 1)[-1].rsplit('```', 1)[0].strip()
        print(f'[HOOK] Raw response: {raw[:200]}', flush=True)
        result = json.loads(raw)
        hook_start = float(result.get('hook_start', 0.0))
        reason = result.get('reason', '')

        # Safety: clamp to 0.0 if hook is negative, beyond transcript, or too aggressive
        last_word_end = words[-1]['end'] if words else 0
        if hook_start < 0 or hook_start > last_word_end or hook_start > max_duration * 0.5:
            print(f'[HOOK] Clamped: {hook_start:.1f}s exceeds max {max_duration * 0.5:.1f}s', flush=True)
            return 0.0

        # Snap to nearest word boundary (start of the closest word at or after hook_start)
        for w in words:
            if w['start'] >= hook_start:
                hook_start = w['start']
                break

        print(f'[HOOK] Skipping {hook_start:.1f}s of intro — {reason}', flush=True)
        return hook_start

    except Exception as e:
        print(f'[HOOK] Failed, using 0.0: {e}', flush=True)
        return 0.0


def _enhance_clip(video_path, tmp_dir, context_hint='', max_duration=60):
    """
    Post-process an encoded clip:
    1. Transcribe with Whisper -> find natural speech cutoff -> animated ASS captions
    2. Detect story with Claude Haiku -> DALL-E image + Ken Burns overlay (conditional)
    Falls back to returning video_path unchanged on any failure.
    Future: replace _make_story_visual() with a video-AI API call (Runway/Luma/Kling).
    """
    try:
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        if not openai_key:
            return video_path, ''

        from openai import OpenAI
        oc = OpenAI(api_key=openai_key)

        # Step 1: Transcribe with Whisper (word-level timestamps)
        # Whisper API has a 25MB file size limit. The encode may be up to
        # max_duration+30s to give the hook detector material — if that pushes
        # past 24MB, create a truncated copy for transcription only.
        whisper_input = video_path
        try:
            file_size = os.path.getsize(video_path)
            if file_size > 24 * 1024 * 1024:  # 24MB safety margin
                whisper_input = os.path.join(tmp_dir, 'whisper_input.mp4')
                subprocess.run([
                    'ffmpeg', '-y', '-i', video_path,
                    '-t', str(max_duration),
                    '-c:v', 'copy', '-c:a', 'copy',
                    '-movflags', '+faststart',
                    whisper_input
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
                if not os.path.exists(whisper_input):
                    whisper_input = video_path  # fallback to original
        except Exception:
            pass  # proceed with original file

        try:
            with open(whisper_input, 'rb') as f:
                transcript = oc.audio.transcriptions.create(
                    model='whisper-1',
                    file=f,
                    response_format='verbose_json',
                    timestamp_granularities=['word']
                )
            # Normalize to dicts — Whisper returns TranscriptionWord Pydantic objects
            words = [{'word': w.word, 'start': w.start, 'end': w.end}
                     for w in (transcript.words or [])]
            full_text = transcript.text or ''
        except Exception:
            return video_path, ''  # can't transcribe = skip enhancement

        if not words:
            return video_path, ''

        # Step 1.5: Detect intro and find hook start (context-aware)
        hook_start = _find_hook_start(words, full_text, context_hint, max_duration)

        # Step 1.6: Find natural speech cutoff, accounting for hook start
        # We want max_duration of CONTENT after the hook, so end = hook_start + max_duration
        absolute_end = hook_start + max_duration
        cutoff = _find_natural_cutoff(words, absolute_end)
        effective_duration = cutoff - hook_start

        # Trim words to [hook_start, cutoff] window, then offset timestamps to start at 0
        words = [w for w in words if w['start'] >= hook_start and w['start'] < cutoff]
        words = [{'word': w['word'], 'start': w['start'] - hook_start, 'end': w['end'] - hook_start}
                 for w in words]
        full_text = ' '.join(w['word'] for w in words)

        # Step 2: Build ASS subtitle file
        subtitles_path = os.path.join(tmp_dir, 'subtitles.ass')
        _build_ass_subtitles(words, subtitles_path)

        # Step 3: Detect story with Claude Haiku
        story_segments = []
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if anthropic_key and full_text.strip():
            try:
                from anthropic import Anthropic
                ac = Anthropic(api_key=anthropic_key)
                resp = ac.messages.create(
                    model='claude-haiku-4-5-20251001',
                    max_tokens=600,
                    messages=[{'role': 'user', 'content': (
                        'Analyze this short podcast transcript (under 30 seconds). '
                        'Does the speaker tell a concrete story, vivid anecdote, or describe a specific scene? '
                        '(NOT just opinions, statistics, or general advice.)\n\n'
                        f'Transcript: "{full_text}"\n\n'
                        'If YES a story is told, return JSON with up to 2 segments:\n'
                        '{"storyboard":true,"segments":[{"start":1.5,"end":6.0,"prompt":"cinematic illustration of [specific scene being described]"}]}\n\n'
                        'If NO story, return: {"storyboard":false}\n\n'
                        'Return only raw JSON, no markdown.'
                    )}]
                )
                story_data = json.loads(resp.content[0].text.strip())
                if story_data.get('storyboard') and story_data.get('segments'):
                    story_segments = story_data['segments'][:2]
            except Exception:
                pass  # captions only if story detection fails

        # Step 4: Generate DALL-E image + Ken Burns overlay per story segment
        overlay_clips = []
        for i, seg in enumerate(story_segments):
            try:
                img_path = _make_story_visual(oc, seg['prompt'], i, tmp_dir)
                if img_path:
                    overlay_clips.append((float(seg['start']), float(seg['end']), img_path))
            except Exception:
                pass

        # Step 5: FFmpeg enhance pass (captions always, overlays if story found)
        enhanced_path = os.path.join(tmp_dir, 'enhanced.mp4')
        success = _run_enhance_ffmpeg(video_path, subtitles_path, overlay_clips, enhanced_path,
                                      cutoff=effective_duration, seek_start=hook_start)
        return (enhanced_path if success else video_path), full_text

    except Exception:
        return video_path, ''  # always fall back to original on unexpected error


def _build_ass_subtitles(words, output_path):
    """Group Whisper word-timestamps into 3-word blocks and write an ASS subtitle file."""
    header = (
        '[Script Info]\n'
        'ScriptType: v4.00+\n'
        'PlayResX: 1080\n'
        'PlayResY: 1920\n\n'
        '[V4+ Styles]\n'
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
        'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, '
        'Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
        'Style: Default,FreeSans,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,'
        '-1,0,0,0,100,100,0,0,1,4,0,2,60,60,80,1\n\n'
        '[Events]\n'
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    )
    events = []
    block = []
    for idx, w in enumerate(words):
        block.append(w)
        next_start = words[idx + 1]['start'] if idx + 1 < len(words) else 9999
        gap = next_start - w['end']
        if len(block) >= 3 or gap > 0.4:
            start_ts = _ass_ts(block[0]['start'])
            end_ts = _ass_ts(block[-1]['end'] + 0.15)
            text = ' '.join(b['word'].strip() for b in block).upper()
            events.append(
                f'Dialogue: 0,{start_ts},{end_ts},Default,,0,0,0,,{{\\fad(80,80)}}{text}'
            )
            block = []
    # flush remaining words
    if block:
        start_ts = _ass_ts(block[0]['start'])
        end_ts = _ass_ts(block[-1]['end'] + 0.15)
        text = ' '.join(b['word'].strip() for b in block).upper()
        events.append(
            f'Dialogue: 0,{start_ts},{end_ts},Default,,0,0,0,,{{\\fad(80,80)}}{text}'
        )
    with open(output_path, 'w') as f:
        f.write(header + '\n'.join(events))


def _ass_ts(seconds):
    """Convert float seconds to ASS timestamp H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def _make_story_visual(oc, prompt, index, tmp_dir):
    """
    Generate a DALL-E 3 image for a story segment and save it locally.
    Future swap point: replace with a video-AI API call (Runway/Luma/Kling)
    to generate an actual animated clip instead of a still image.
    Returns local image path, or None on failure.
    """
    import requests as req_lib
    resp = oc.images.generate(
        model='dall-e-3',
        prompt=f'Cinematic illustration, muted atmospheric colors, no text, no words: {prompt}',
        size='1024x1792',
        quality='standard',
        n=1
    )
    img_url = resp.data[0].url
    img_path = os.path.join(tmp_dir, f'story_{index}.png')
    img_data = req_lib.get(img_url, timeout=30).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def _run_enhance_ffmpeg(video_path, subtitles_path, overlay_clips, output_path, cutoff=None, seek_start=0.0):
    """
    Build and run the FFmpeg enhancement pass.
    - overlay_clips: list of (start_sec, end_sec, image_path) for Ken Burns overlays
    - Always burns in ASS captions
    - cutoff: trim output to this duration (natural speech boundary)
    - seek_start: skip this many seconds from the start (intro skip)
    Returns True if output file was created successfully.
    """
    duration_flag = ['-t', str(cutoff)] if cutoff is not None else []
    seek_flag = ['-ss', str(seek_start)] if seek_start > 0 else []

    def _run_ffmpeg_safe(cmd, timeout_s):
        """Run ffmpeg via Popen+DEVNULL to avoid capture_output pipe deadlock on timeout."""
        with subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as proc:
            try:
                proc.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return False
        return proc.returncode == 0 and os.path.exists(output_path)

    if not overlay_clips:
        # Captions only — simple -vf filter
        cmd = [
            'ffmpeg', '-y',
        ] + seek_flag + [
            '-i', video_path,
            '-vf', f'ass={subtitles_path}',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'copy', '-movflags', '+faststart',
        ] + duration_flag + [output_path]
        return _run_ffmpeg_safe(cmd, timeout_s=180)

    # Build filter_complex: Ken Burns animated overlays + captions
    inputs = seek_flag + ['-i', video_path]
    filter_parts = []

    for i, (start, end, img_path) in enumerate(overlay_clips):
        duration = max(0.5, end - start)
        frames = max(30, int(duration * 30))
        inputs += ['-loop', '1', '-t', str(duration + 0.5), '-i', img_path]
        # Slow zoom from 1.0 to 1.2 (Ken Burns) + 45% opacity
        filter_parts.append(
            f'[{i + 1}:v]scale=1200:2133,'
            f'zoompan=z=\'min(1+0.0015*n,1.2)\':'
            f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':'
            f'd={frames}:s=1080x1920:fps=30,'
            f'format=rgba,colorchannelmixer=aa=0.45[img{i}]'
        )

    # Convert main video to rgba and chain overlays
    filter_parts.append('[0:v]format=rgba[v0]')
    current = 'v0'
    for i, (start, end, _) in enumerate(overlay_clips):
        nxt = f'v{i + 1}'
        is_last = (i == len(overlay_clips) - 1)
        fmt = 'yuv420p' if is_last else 'rgba'
        filter_parts.append(
            f'[{current}][img{i}]overlay=0:0:enable=\'between(t,{start},{end})\','
            f'format={fmt}[{nxt}]'
        )
        current = nxt

    # Burn captions on top of everything
    filter_parts.append(f'[{current}]ass={subtitles_path}[out]')

    cmd = (
        ['ffmpeg', '-y'] + inputs +
        [
            '-filter_complex', ';'.join(filter_parts),
            '-map', '[out]', '-map', '0:a',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'copy', '-movflags', '+faststart',
        ] + duration_flag + [output_path]
    )
    return _run_ffmpeg_safe(cmd, timeout_s=300)


@app.route('/download-clip', methods=['POST'])
def download_clip():
    data = request.get_json(force=True) or {}
    query = data.get('query', '').strip()
    niche_slug = data.get('niche_slug', 'content').strip()
    date = data.get('date', datetime.now().strftime('%Y-%m-%d')).strip()
    index = data.get('index', 1)
    max_duration = int(data.get('max_duration', 60))

    if not query:
        return jsonify({'success': False, 'error': 'query is required'}), 400

    excluded_urls = data.get('excluded_urls', [])
    result = _do_download(query, niche_slug, date, index, max_duration, excluded_urls)
    return jsonify(result)


@app.route('/download-clips-batch', methods=['POST'])
def download_clips_batch():
    """Download multiple clips in parallel. Accepts {clips: [{query, niche_slug, date, index, max_duration}]}"""
    data = request.get_json(force=True) or {}
    clips = data.get('clips', [])

    if not clips:
        return jsonify({'success': False, 'error': 'clips array is required'}), 400

    def download_one(clip_data):
        return _do_download(
            query=clip_data.get('query', '').strip(),
            niche_slug=clip_data.get('niche_slug', 'content').strip(),
            date=clip_data.get('date', datetime.now().strftime('%Y-%m-%d')).strip(),
            index=clip_data.get('index', 1),
            max_duration=int(clip_data.get('max_duration', 60))
        )

    results = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(download_one, clip): i for i, clip in enumerate(clips)}
        for future in as_completed(futures):
            results.append(future.result())

    # Sort by original index so order matches input
    results.sort(key=lambda x: x.get('index', 0))

    return jsonify({'success': True, 'clips': results})


def _generate_card(title, niche_slug, date, index, subtitle=None, bg_color='#1A2330', text_color='#FFFFFF', logo_path=None, style='document', hook_label=''):
    """
    Generate a branded 1080×1080 PNG image card using HTML/CSS rendered via Playwright.

    The card template (card_template.html) includes:
    - Burnham logo (top-left)
    - Navy gradient background (#1A2330 to #263340)
    - Gold divider line
    - EB Garamond headline (white, 72px)
    - Inter subtitle (gold, 38px)
    - Gold footer bar with burnhamandsons.com

    Args:
        title: Card headline (fills <!--TITLE--> placeholder)
        niche_slug: Workflow name slug (e.g., 'burnham-insurance')
        date: YYYY-MM-DD for file organization
        index: Post index (for filename uniqueness)
        subtitle: Card subheading (fills <!--SUBTITLE-->, optional)
        bg_color, text_color, logo_path: Unused (kept for API compatibility)

    Returns:
        dict: {'success': True, 'filename': '...', 'public_url': '...'} or {'success': False, 'error': '...'}
    """
    try:
        import time as _time
        from playwright.sync_api import sync_playwright

        # Setup directories
        output_dir = os.path.join(BASE_OUTPUT_DIR, date)
        os.makedirs(output_dir, exist_ok=True)

        epoch = int(_time.time())
        filename = f'{niche_slug}-{date}-{index}-{epoch}.png'
        output_path = os.path.join(output_dir, filename)
        tmp_dir = tempfile.mkdtemp()

        # Load template based on style
        template_file = '/app/card_template_hook.html' if style == 'hook' else '/app/card_template.html'
        with open(template_file, 'r') as f:
            html = f.read()

        html = html.replace('<!--TITLE-->', title)
        html = html.replace('<!--SUBTITLE-->', subtitle or '')
        html = html.replace('<!--HOOK_LABEL-->', hook_label)

        # Write filled HTML to temp file
        tmp_html = os.path.join(tmp_dir, 'card.html')
        with open(tmp_html, 'w') as f:
            f.write(html)

        # Render HTML to PNG using Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1080, 'height': 1080})
            # Use file:// URL and wait for fonts to load
            page.goto(f'file://{tmp_html}', wait_until='networkidle')
            # Hide the footer badge if it overlaps the subtitle text
            page.evaluate("""
                () => {
                    const subtitle = document.querySelector('.subtitle');
                    const footer = document.querySelector('.footer');
                    if (subtitle && footer) {
                        const subtitleBottom = subtitle.getBoundingClientRect().bottom;
                        const footerTop = footer.getBoundingClientRect().top;
                        if (subtitleBottom > footerTop - 20) {
                            footer.style.display = 'none';
                        }
                    }
                }
            """)
            page.screenshot(path=output_path)
            browser.close()

        public_url = f'{PUBLIC_BASE_URL}/{date}/{filename}'
        return {
            'success': True,
            'filename': filename,
            'public_url': public_url,
            'output_path': output_path,
            'index': index,
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'index': index,
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@app.route('/generate-card', methods=['POST'])
def generate_card():
    """
    Generate a branded image card for social media posts.
    Request body: {title, subtitle?, niche_slug, date, index, bg_color?, text_color?, logo_path?, style?, hook_label?}
    """
    data = request.get_json(force=True) or {}
    title = data.get('title', '').strip()
    subtitle = data.get('subtitle', '').strip() or None
    niche_slug = data.get('niche_slug', 'content').strip()
    date = data.get('date', datetime.now().strftime('%Y-%m-%d')).strip()
    index = data.get('index', 1)
    bg_color = data.get('bg_color', '#1A2330').strip()
    text_color = data.get('text_color', '#FFFFFF').strip()
    logo_path = data.get('logo_path')
    style = data.get('style', 'document').strip()
    hook_label = data.get('hook_label', '').strip()

    if not title:
        return jsonify({'success': False, 'error': 'title is required'}), 400

    result = _generate_card(title, niche_slug, date, index, subtitle, bg_color, text_color, logo_path, style, hook_label)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
