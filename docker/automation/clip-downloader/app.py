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
PUBLIC_BASE_URL = 'https://media.burnhamandsons.com'


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


def _do_download(query, niche_slug, date, index, max_duration):
    """Core clip download logic. Returns a result dict."""
    if not query:
        return {'success': False, 'error': 'query is required', 'index': index}

    output_dir = os.path.join(BASE_OUTPUT_DIR, date)
    os.makedirs(output_dir, exist_ok=True)
    filename = f'{niche_slug}-{date}-{index}.mp4'
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path):
        os.remove(output_path)

    tmp_dir = tempfile.mkdtemp()
    tmp_output = os.path.join(tmp_dir, 'raw.%(ext)s')

    try:
        def _run_yt(search_q, use_duration_filter, timeout_s):
            """Run yt-dlp and return (result, source_title, source_url, source_duration, raw_file)."""
            cmd = [
                'yt-dlp',
                '--no-playlist',
                '--format', 'best[height<=720]/best[height<=480]/worst[ext=mp4]/worst',
                '--download-sections', f'*0:00-{max_duration}',
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
                    break
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
            f'ytsearch3:{query}', use_duration_filter=True, timeout_s=240
        )

        # Fallback 1: append "shorts clip" and try 5 results, no hard duration filter
        # (match-filter already applied above; fallback is more permissive to find anything)
        if not raw_file:
            _, source_title, source_url, _, raw_file = _run_yt(
                f'ytsearch5:{query} shorts clip', use_duration_filter=False, timeout_s=240
            )

        # Fallback 2: simplified query (first 6 words), no duration check at all.
        # The full combined query (youtube_search_query + suffix) can be 10+ words —
        # too specific for YouTube to return any results. Truncating to 6 words gives
        # a broader search that almost always finds something. ffmpeg -t still trims to
        # max_duration regardless of source video length.
        if not raw_file:
            def _run_yt_any(search_q, timeout_s):
                """Like _run_yt but skips the s_dur > 600 rejection."""
                cmd = [
                    'yt-dlp',
                    '--no-playlist',
                    '--format', 'best[height<=720]/best[height<=480]/worst[ext=mp4]/worst',
                    '--download-sections', f'*0:00-{max_duration}',
                    '--print', 'before_dl:%(title)s|||%(webpage_url)s|||%(duration)s',
                    '-o', tmp_output,
                    search_q,
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=tmp_dir)
                s_title, s_url = '', ''
                for line in res.stdout.splitlines():
                    if '|||' in line:
                        parts = line.split('|||')
                        s_title = parts[0].strip() if len(parts) > 0 else ''
                        s_url   = parts[1].strip() if len(parts) > 1 else ''
                        break
                r_file = None
                for f in os.listdir(tmp_dir):
                    if f.startswith('raw.') and not f.endswith('.part'):
                        r_file = os.path.join(tmp_dir, f)
                        break
                return s_title, s_url, r_file

            # Use first 6 words of the query — the full combined string is often too
            # specific and returns zero YouTube results.
            short_q = ' '.join(query.split()[:6])
            source_title, source_url, raw_file = _run_yt_any(
                f'ytsearch1:{short_q}', timeout_s=180
            )

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
            '-t', str(max_duration),
            tmp_encoded
        ]

        ff_result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if ff_result.returncode != 0 or not os.path.exists(tmp_encoded):
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
                '-t', str(max_duration),
                tmp_encoded
            ]
            ff_result2 = subprocess.run(
                ffmpeg_cmd_simple,
                capture_output=True,
                text=True,
                timeout=300
            )
            if ff_result2.returncode != 0 or not os.path.exists(tmp_encoded):
                return {
                    'success': False,
                    'error': f'ffmpeg failed: {ff_result2.stderr[-500:]}',
                    'index': index
                }

        # Enhance with captions + optional storyboard overlay, then copy to NAS
        enhanced = _enhance_clip(tmp_encoded, tmp_dir, query)
        shutil.copy2(enhanced, output_path)

        public_url = f'{PUBLIC_BASE_URL}/{date}/{filename}'

        return {
            'success': True,
            'filename': filename,
            'public_url': public_url,
            'source_title': source_title,
            'source_url': source_url,
            'output_path': output_path,
            'index': index
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


def _enhance_clip(video_path, tmp_dir, context_hint=''):
    """
    Post-process an encoded clip:
    1. Transcribe with Whisper -> animated ASS captions (always)
    2. Detect story with Claude Haiku -> DALL-E image + Ken Burns overlay (conditional)
    Falls back to returning video_path unchanged on any failure.
    Future: replace _make_story_visual() with a video-AI API call (Runway/Luma/Kling).
    """
    try:
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        if not openai_key:
            return video_path

        from openai import OpenAI
        oc = OpenAI(api_key=openai_key)

        # Step 1: Transcribe with Whisper (word-level timestamps)
        try:
            with open(video_path, 'rb') as f:
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
            return video_path  # can't transcribe = skip enhancement

        if not words:
            return video_path

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
        success = _run_enhance_ffmpeg(video_path, subtitles_path, overlay_clips, enhanced_path)
        return enhanced_path if success else video_path

    except Exception:
        return video_path  # always fall back to original on unexpected error


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


def _run_enhance_ffmpeg(video_path, subtitles_path, overlay_clips, output_path):
    """
    Build and run the FFmpeg enhancement pass.
    - overlay_clips: list of (start_sec, end_sec, image_path) for Ken Burns overlays
    - Always burns in ASS captions
    Returns True if output file was created successfully.
    """
    if not overlay_clips:
        # Captions only — simple -vf filter
        cmd = [
            'ffmpeg', '-y', '-i', video_path,
            '-vf', f'ass={subtitles_path}',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'copy', '-movflags', '+faststart',
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        return result.returncode == 0 and os.path.exists(output_path)

    # Build filter_complex: Ken Burns animated overlays + captions
    inputs = ['-i', video_path]
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
            output_path
        ]
    )
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return result.returncode == 0 and os.path.exists(output_path)


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

    result = _do_download(query, niche_slug, date, index, max_duration)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
