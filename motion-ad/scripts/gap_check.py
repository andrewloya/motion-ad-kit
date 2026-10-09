#!/usr/bin/env python3
"""gap_check.py <render.mp4> [--from A --to B] [--max 170] [--hold 0.4] — dead gaps BETWEEN things on screen.
From the LYRC build (the PHASE? hook, ~240 px of black between "CALLS IT A" and "PHASE?"): "spacing is a vital thing… never leave
too much gap between shit". fill_check catches a whole empty third; this catches the smaller hole between two stacked
elements: a horizontal band of empty rows (edge energy near zero, texture and grain ignored) taller than --max px (at
1920 high) with content above AND below it, held ≥ --hold s. Margins at the very top/bottom don't count."""
import sys, numpy as np, cv2
a = sys.argv; src = a[1]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
t0, t1, MAX, HOLD = opt('--from', 0), opt('--to', 1e9), opt('--max', 170), opt('--hold', 0.4)
imgs = [x for x in a[1:] if x.lower().endswith('.png')]                    # stills too: gap_check.py frame-*.png
if imgs:
    class _C:                                                                # serve the PNGs as a 1-fps "video"
        def __init__(s): s.i = 0
        def get(s, p): return 1.0 if p == cv2.CAP_PROP_FPS else len(imgs)
        def set(s, p, v): s.i = int(v)
        def read(s): return (s.i < len(imgs), cv2.imread(imgs[s.i]) if s.i < len(imgs) else None)
    cap, HOLD = _C(), 0
else:
    cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
step = max(1, int(round(fps / 10)))                                          # 10 samples/s
hits = []
for i in range(int(t0 * fps), min(n, int(t1 * fps)), step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
    if not ok: break
    H = f.shape[0]; k = 1920 / H
    g = cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (5, 5), 0).astype(np.float32)
    e = np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)) + np.abs(cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    busy = (e > 18).mean(1) > 0.003                                          # rows with real detail (type, figures, footage, a big glyph's sides)
    run = np.convolve(busy.astype(float), np.ones(int(24 / k) or 1), "same")
    busy &= run >= max(1, int(24 / k) * 0.75)                                # a lone speck or a hairline isn't content (text and figures run 24 px+)
    idx = np.flatnonzero(busy)
    idx = idx[(idx * k > 120) & (idx * k < 1800)]                            # the frame's top/bottom edges are margins, not gaps
    if len(idx) < 2: continue
    best = 0; bi = None
    for j in range(len(idx) - 1):                                            # empty runs between the first and last busy row
        gap = (idx[j + 1] - idx[j]) * k
        if gap > best: best, bi = gap, (idx[j] * k, idx[j + 1] * k)
    hits.append((i / fps, best, bi))
bad = []; run = []
for t, gap, b in hits:
    if gap > MAX and imgs: print(f'GAP in {imgs[int(t)]}: {gap:.0f} px between y {b[0]:.0f} and {b[1]:.0f}')
    if gap > MAX: run.append((t, gap, b))
    else:
        if run and run[-1][0] - run[0][0] >= HOLD: bad.append(run)
        run = []
if run and run[-1][0] - run[0][0] >= HOLD: bad.append(run)
for r in bad:
    g = max(r, key=lambda x: x[1])
    print(f'GAP {r[0][0]:.2f}–{r[-1][0]:.2f} s: up to {g[1]:.0f} px empty between y {g[2][0]:.0f} and {g[2][1]:.0f} (at {g[0]:.2f} s)')
print('ok' if not bad else f'{len(bad)} stretch(es) with a gap over {MAX:.0f} px')
