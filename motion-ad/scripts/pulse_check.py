#!/usr/bin/env python3
"""Does the camera pulse to the beat? Finds short, whole-frame zoom bumps in a render.

uv run --with numpy --with opencv-python-headless python <skill>/scripts/pulse_check.py <video.mp4>
From the LYRC build, on a version with camera surges on hits, hat pushes and breathing glows: "we need to not do the pulsing to the beat."
A bump = the whole frame zooms (optical flow fits a zoom well) for ≤0.2 s. One bump on its own is an event (a slam,
the start of a dive) and is fine. Pulsing = bumps repeating: two within 1.2 s of each other, or more than 4 in the ad.
Calibrated on the LYRC ads: the rejected cut had 8 bumps (on the hats → fail); the fixed one 3, all isolated; loved ads 0–2.
It sees camera/zoom pulses only; glows and scale "breathing" on single elements are caught by craft_check (yoyo/repeat).
Exit 1 when it pulses.
"""
import subprocess, sys
import numpy as np
import cv2

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
vid, fps, W, H = sys.argv[1], 15, 216, 384
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', vid, '-vf', f'fps={fps},scale={W}:{H},format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
ys, xs = np.mgrid[3:H:6, 3:W:6].astype(float)
dx, dy = (xs - W / 2).ravel(), (ys - H / 2).ravel()
A = np.zeros((2 * len(dx), 3)); A[:len(dx), 0] = dx; A[len(dx):, 0] = dy; A[:len(dx), 1] = 1; A[len(dx):, 2] = 1
z, fit = [], []
for a, b in zip(fr[:-1], fr[1:]):
    f = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    y = np.concatenate([f[3::6, 3::6, 0].ravel(), f[3::6, 3::6, 1].ravel()])
    p = np.linalg.lstsq(A, y, rcond=None)[0]
    z.append(p[0] * 100); fit.append(1 - ((y - A @ p) ** 2).sum() / (((y - y.mean()) ** 2).sum() + 1e-9))
z, fit = np.array(z), np.array(fit)
hi = (np.abs(z) > 0.6) & (fit > 0.5)
bumps, i = [], 0
while i < len(z):
    if hi[i]:
        j = i
        while j + 1 < len(z) and hi[j + 1]:
            j += 1
        if j - i + 1 <= 3:
            bumps.append(round((i + 1) / fps, 2))
        i = j + 1
    else:
        i += 1
close = [(a, b) for a, b in zip(bumps, bumps[1:]) if b - a < 1.2]
print(f'zoom bumps {len(bumps)} at {bumps} · repeating pairs (<1.2 s apart) {close}')
bad = bool(close) or len(bumps) > 4
print('PULSING TO THE BEAT: remove the repeated pushes/bumps; keep at most one hit per big event (from the LYRC build)' if bad else 'ok')
sys.exit(1 if bad else 0)
