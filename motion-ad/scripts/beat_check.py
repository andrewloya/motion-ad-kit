#!/usr/bin/env python3
"""Are the footage cuts on the beat? Fits a constant-tempo beat grid to the song, finds every hard cut in a render,
and prints each cut's distance to the nearest beat.

uv run --with librosa --with numpy python scripts/beat_check.py <render.mp4> --audio <song master.wav> --song-start S
    [--from A --to B] [--fps 60] [--grid-out grid.json]
--song-start: song time at the render's t=0 (where the ad's audio starts inside the track).
--from/--to: render-time window to check. Keep it to stretches where the picture changes only at footage cuts: a big
  lyric word swapping in fills the frame too and reads as a "cut" (Duet/Overdrive words, line changes).
--grid-out: writes {"P": beat period s, "T0": song time of beat 0, "bpm"} for placing cuts (beat k = T0 + P*k).
Exit 1 when the mean |error| is over 35 ms or any cut is over 60 ms off (1 frame at 30 fps = 33 ms).

Why (from the LYRC build): "the cuts for the vids are not on beat. they need to be". A stored BPM and hand-placed
markers sat 40–200 ms off the beat (120 BPM stored for a 132 BPM track), and the cuts copied them.
Put cuts on this grid (bar starts for hero shots, every 2 beats for fast tile walls), then check the final render here.
"""
import json, subprocess, sys
import numpy as np

a = sys.argv[1:]
if not a or a[0] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
vid, audio = a[0], opt('--audio')
off = float(opt('--song-start', '0')); lo = float(opt('--from', '0')); hi = float(opt('--to', '1e9'))
fps = int(opt('--fps', '60'))
if not audio:
    print('--audio <song master> is required'); sys.exit(2)

import librosa
y, sr = librosa.load(audio, sr=22050, mono=True)
oenv = librosa.onset.onset_strength(y=y, sr=sr)
_, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, units='time', tightness=200)
# fit only around the checked window (the tracker wanders in intros/outros), counting beats step by step so one
# skipped or doubled beat doesn't bend the line, then refit without outliers
w0, w1 = off + lo - 6, off + min(hi, 600) + 6
b = beats[(beats > w0) & (beats < w1)]
if len(b) < 12:
    b = beats
ibi = np.median(np.diff(b))
k = np.concatenate([[0], np.cumsum(np.maximum(1, np.round(np.diff(b) / ibi)))])
for _ in range(3):
    P, T0 = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, b, rcond=None)[0]
    res = b - (T0 + P * k)
    keep = np.abs(res) < max(0.04, 2.5 * np.sqrt((res ** 2).mean()))
    b, k = b[keep], k[keep]
T0 = T0 - P * np.ceil(T0 / P)   # beat 0 near song start, same grid
print(f'grid {60 / P:.2f} bpm, fit rms {np.sqrt((res[keep] ** 2).mean()) * 1000:.0f} ms over {len(b)} beats')
if opt('--grid-out'):
    json.dump({'P': float(P), 'T0': float(T0), 'bpm': float(60 / P)}, open(opt('--grid-out'), 'w'))
grid = T0 + P * np.arange(-200, 2000)

W, H = 90, 160
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', vid, '-vf', f'fps={fps},scale={W}:{H},format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
h = np.array([np.histogram(f, bins=32, range=(0, 255))[0] / f.size for f in fr])
d = np.abs(np.diff(h, axis=0)).sum(1)
errs = []
for i in range(1, len(d) - 1):
    if d[i] > 0.35 and d[i] > 2.5 * max(d[i - 1], d[i + 1], 0.02):
        t = (i + 1) / fps
        if not (lo <= t <= hi):
            continue
        s = off + t
        e = (s - grid[np.argmin(np.abs(grid - s))]) * 1000
        errs.append(e)
        print(f'cut at {t:7.3f} s (song {s:7.3f})  {e:+5.0f} ms from beat')
if not errs:
    print('no cuts found in the window'); sys.exit(0)
ok = np.mean(np.abs(errs)) <= 35 and max(map(abs, errs)) <= 60
print(f'{len(errs)} cuts · mean |error| {np.mean(np.abs(errs)):.0f} ms · max {max(map(abs, errs)):.0f} ms — '
      + ('ok' if ok else 'OFF THE BEAT: move the cuts onto the grid (--grid-out), or narrow --from/--to past lyric swaps'))
sys.exit(0 if ok else 1)
