#!/usr/bin/env python3
"""Is the ad too fast / too much going on? Measures how often NEW stuff arrives, not how much things move.

uv run --with numpy --with opencv-python-headless python <skill>/scripts/pace_check.py <video.mp4> [--narrated | --hook] [--allow a-b]
- calm time: % of 0.1 s steps with no new content. Each frame is predicted from the last one by optical flow, so a
  camera push, parallax, a word sliding or a letter bouncing still counts as calm. A cut, a new element or a new
  screen doesn't. Rich motion is wanted (craft_check.py measures it); too many new things is the failure.
- longest rush: the longest stretch with no calm moment of ≥0.5 s.
Calibrated on the LYRC build's verdicts:
  an ad called "a lot better" 75% / rush 2.0 s · one called "SO FUCKING GOOD" (music-driven) 44%
  one test went 40% → 25% → 22% / rush 14.3 s → "way too fast and too much going on"; at 66% / 3.0 s its pace was OK
Bars: narrated calm ≥ 30% and longest rush ≤ 3.5 s (people are listening AND reading); music-driven calm ≥ 30%.
  Recalibrated: 22% was "way too fast"; THE bar ad (examples/worse-song) at 33%
  was "so much better" and then "the ideal motion graphic video". What he rejects is JUMBLED (layers fighting, words
  over busy texture, fast cutting in a story moment) and DEAD (holds with nothing new), which this number can't see:
  the critic judges those by eye. Under 30% is still too much.
--hook (a hook render): ADVISORY, always exits 0. the LYRC build called three fast story hooks "insanely better… fire"
  and they measure 0–9% calm; the hook's job is to be the most engaging part, as long as every printed word reads.
  (Earlier calm hooks that were liked: 51%, 72%. Both kinds work; slow isn't the goal in a hook.)
Too fast? Cut beats (fewer steps, one idea per scene) and hold each key visual 2–3 s, still animating. Don't speed up.
--allow: ONE payoff picture that is busy by nature but is a single idea (the 30-video wall: 30 tiles playing at once),
  ≤3 s in total, counted as calm. Never use it to wave through a fast sequence. v7 dimmed its wall to black to pass
  an earlier version of this gate, and that killed the payoff: allow the wall instead and keep it lit.
Exit 1 when under the bar.
"""
import subprocess, sys
import numpy as np
import cv2

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
vid, narrated, fps, W, H = sys.argv[1], '--narrated' in sys.argv, 10, 216, 384
ALLOW = [tuple(float(x) for x in r.split('-')) for r in (sys.argv[sys.argv.index('--allow') + 1].split(',') if '--allow' in sys.argv else [])]
allowed = sum(b - a for a, b in ALLOW)
if allowed > 3.0:
    print(f'--allow covers {allowed:.1f} s; the limit is 3 s (one payoff picture)'); sys.exit(2)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', vid, '-vf', f'fps={fps},scale={W}:{H},format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
resid = []
for a, b in zip(fr[:-1], fr[1:]):
    flow = cv2.calcOpticalFlowFarneback(b, a, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    pred = cv2.remap(a, gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    resid.append(np.abs(b.astype(float) - pred).mean())
calm = np.array(resid) < 2.5
for i in range(len(calm)):
    if any(a <= (i + 1) / fps <= b for a, b in ALLOW):
        calm[i] = True
dur = len(fr) / fps
rush, best, best_at, run = 0, 0, 0, 0
for i, c in enumerate(calm):
    run = run + 1 if c else 0
    if run >= 5:
        rush = 0
    else:
        rush += 1
        if rush > best:
            best, best_at = rush, i
calm_pct = 100 * calm.mean()
hook = '--hook' in sys.argv
bar_calm, bar_rush = (45, 2.5) if hook else (30, 3.5) if narrated else (30, 99)
print(f'calm time {calm_pct:.0f}% (bar {bar_calm}%) · longest rush {best / fps:.1f} s ending at {best_at / fps:.1f} s'
      f'{f" (bar {bar_rush} s)" if bar_rush < 99 else ""} · {dur:.1f} s{f" · allowed {allowed:.1f} s" if ALLOW else ""}')
ok = hook or (calm_pct >= bar_calm and best / fps <= bar_rush)
print('ok' if ok else 'TOO FAST / TOO MUCH: cut beats and hold the key visuals longer (from the LYRC build: "way too fast and too much going on")')
sys.exit(0 if ok else 1)
