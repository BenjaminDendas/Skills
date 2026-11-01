#!/usr/bin/env python3
"""Helpers for the narrate-video skill. Subcommands: ffmpeg, sheets, audio, mux."""
import argparse, glob, io, json, os, shutil, subprocess, sys, urllib.request

def ffmpeg_path():
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"])
        import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def duration(ff, video):
    r = subprocess.run([ff, "-i", video], capture_output=True, text=True).stderr
    for l in r.splitlines():
        if "Duration:" in l:
            h, m, s = l.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    sys.exit("could not read duration")

def cmd_sheets(a):
    ff = ffmpeg_path(); os.makedirs(a.workdir, exist_ok=True)
    for f in glob.glob(os.path.join(a.workdir, "s_*.png")): os.remove(f)
    subprocess.check_call([ff, "-v", "error", "-i", a.video, "-vf", "fps=1,scale=260:-1,tile=6x2",
                           os.path.join(a.workdir, "s_%02d.png")])
    print(f"duration {duration(ff, a.video):.2f}s")
    for f in sorted(glob.glob(os.path.join(a.workdir, "s_*.png"))): print(f)

def cmd_audio(a):
    import numpy as np, soundfile as sf
    ff = ffmpeg_path(); SR = 24000
    total = duration(ff, a.video)
    segs = sorted(json.load(open(a.script)), key=lambda s: s["start"])
    def tts(t, sp):
        r = urllib.request.Request(f"{a.api}/tts", json.dumps({"text": t, "voice": a.voice, "speed": sp}).encode(),
                                   {"content-type": "application/json"})
        x, sr = sf.read(io.BytesIO(urllib.request.urlopen(r, timeout=120).read())); assert sr == SR
        return x.astype("float32")
    out = np.zeros(int((total + 1) * SR), dtype="float32"); over = 0
    for i, s in enumerate(segs):
        end = segs[i + 1]["start"] - 0.15 if i + 1 < len(segs) else total - 0.1
        sp = 1.0
        while True:
            x = tts(s["text"], sp)
            if len(x) / SR <= end - s["start"] or sp >= 1.3: break
            sp = round(sp + 0.05, 2)
        flag = "OVER" if len(x) / SR > end - s["start"] else ""
        over += bool(flag)
        print(f'{s["start"]:6.1f} dur {len(x)/SR:4.1f} slot {end-s["start"]:4.1f} speed {sp} {flag}')
        st = int(s["start"] * SR); out[st:st + len(x)] += x
    tmp = a.out + ".raw.wav"
    sf.write(tmp, out[:int(total * SR)], SR)
    subprocess.check_call([ff, "-y", "-v", "error", "-i", tmp, "-af",
                           "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,pan=stereo|c0=c0|c1=c0",
                           "-c:a", "pcm_s16le", a.out])
    os.remove(tmp)
    print(f"wrote {a.out}; {over} line(s) OVER their slot")

def cmd_mux(a):
    ff = ffmpeg_path()
    subprocess.check_call([ff, "-y", "-v", "error", "-i", a.video, "-i", a.audio, "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                           "-movflags", "+faststart", "-t", f"{duration(ff, a.video):.2f}", a.out])
    print("wrote", a.out)

p = argparse.ArgumentParser(); sp = p.add_subparsers(dest="c", required=True)
sp.add_parser("ffmpeg").set_defaults(f=lambda a: print(ffmpeg_path()))
s = sp.add_parser("sheets"); s.add_argument("video"); s.add_argument("workdir"); s.set_defaults(f=cmd_sheets)
s = sp.add_parser("audio"); s.add_argument("script"); s.add_argument("video"); s.add_argument("out")
s.add_argument("--voice", default="af_heart"); s.add_argument("--api", default="http://127.0.0.1:8000"); s.set_defaults(f=cmd_audio)
s = sp.add_parser("mux"); s.add_argument("video"); s.add_argument("audio"); s.add_argument("out"); s.set_defaults(f=cmd_mux)
a = p.parse_args(); a.f(a)
