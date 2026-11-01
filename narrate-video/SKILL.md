---
name: narrate-video
description: Analyse a video (e.g. an app screen recording), write a timed narration script, generate the voiceover with the local Kokoro TTS service, and mux it into a new MP4 with ffmpeg. Use when the user gives a video and wants narration, a voiceover, or audio added to it.
---

# narrate-video

Turns a silent video into a narrated one. The original is never modified. Helper: `.claude/skills/narrate-video/scripts/narrate.py` (run with `.venv/bin/python -I`, from the repo root).

## Steps

1. **Ask first** (AskUserQuestion, one call): voice (`af_heart` warm female default, `am_adam` male, `af_bella` polished), style (step-by-step tutorial / promo voiceover / short captions), and note that Kokoro is English-only. Output is always WAV + merged MP4.
2. **Ensure ffmpeg**: `.venv/bin/python -I .claude/skills/narrate-video/scripts/narrate.py ffmpeg` prints a path (system ffmpeg, else installs `imageio-ffmpeg` into `.venv`).
3. **Analyse the video**: `narrate.py sheets <video> <workdir>` writes contact sheets (12 frames each, 1 frame/s, 6x2) and prints duration. Sheet *n* covers seconds `12(n-1)`..`12n-1`. Put `<workdir>` in the scratchpad. Read every sheet with the Read tool and note what happens at which second (screens, taps, typing, scrolling).
4. **Write the script** as timed lines (start second + text), ~2.5 words/s at normal speed. Start each line when the action begins, keep lines short enough for their slot (until the next line), and leave the video's last second free.
5. **Show the script to the user (table: time / on screen / narration) and wait for approval.** Never generate audio before approval.
6. **Check the TTS server**: `curl -s localhost:8000/health` must show `tts_loaded: true`; otherwise tell the user to start `.venv/bin/uvicorn server:app --port 8000`.
7. **Generate audio**: save the approved script as JSON `[{"start": 0.0, "text": "..."}]`, then
   `narrate.py audio <script.json> <video> outputs/<name>_narration.wav --voice af_heart`.
   Each line is synthesised separately and placed at its start; if it overruns its slot, speed is raised in 0.05 steps up to 1.3. The script prints per-line duration/slot/speed and flags `OVER`. Fix OVER lines by shortening the text or moving starts, then rerun. The WAV is loudness-normalised (-16 LUFS), 48 kHz stereo.
8. **Mux**: `narrate.py mux <video> outputs/<name>_narration.wav outputs/<name>_narrated.mp4` (video stream copied, AAC 192k 48 kHz stereo, faststart, trimmed to video length).
9. **Report** file paths, any sped-up lines, and note the audio has been level-checked but not listened to. If the user hears nothing, check `ffmpeg -i out.mp4 -af volumedetect` and the player.

## Rules
- Outputs go in `outputs/` (gitignored); never overwrite the input video.
- Narrate what is actually on screen; do not invent features.
- TTS runs on the local API (`/tts`, 24 kHz mono WAV), so no network or cloud service is involved.
