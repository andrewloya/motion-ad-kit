#!/usr/bin/env python3
"""Flag stretches where a big part of the frame is dead: flat black / flat white / flat colour with nothing in it.

uv run --with numpy --with pillow python <skill>/scripts/fill_check.py <video.mp4> [--step 0.25] [--hold 1.0] [--allow 23.5-26.5,…]
Splits every frame into 12 cells and calls a cell DEAD when it is nearly flat (no edges, no tonal variation): no
footage, no UI, no type in it. A stretch where a dead
region covers ≥ ⅓ of the frame for ≥ --hold seconds is flagged. From the LYRC build: a narrated test
had 3 small tiles on black and an end card in the top third over empty black; the hook alone was full.
--allow: a DELIBERATE typographic beat (a "line" beat: big centred type ≤3 s on black) is fine —
declare its range. Calibrated on the LYRC ads: a loved ad flags only its line beat; a rejected narrated test flagged 5 stretches.
Exit 1 when anything unallowed is flagged.
"""
import io, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
vid = sys.argv[1]
opt = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
step, hold = opt('--step', 0.25), opt('--hold', 1.0)
ALLOW = [tuple(float(x) for x in r.split('-')) for r in (sys.argv[sys.argv.index('--allow') + 1].split(',') if '--allow' in sys.argv else [])]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid],
                           capture_output=True, text=True).stdout.strip())


def dead_fraction(im):
    g = np.asarray(im.convert('L').resize((108, 192)).filter(ImageFilter.FIND_EDGES)).astype(float)
    lum = np.asarray(im.convert('L').resize((108, 192))).astype(float)
    # 12 cells (4 rows × 3 cols); a cell is dead when it has almost no edges and almost no tonal variation
    dead = 0
    for r in range(4):
        for c in range(3):
            e = g[r * 48:(r + 1) * 48, c * 36:(c + 1) * 36]
            l = lum[r * 48:(r + 1) * 48, c * 36:(c + 1) * 36]
            if e.mean() < 6 and l.std() < 10:
                dead += 1
    return dead / 12


rows, t = [], 0.0
while t < dur - 0.02:
    png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', '-f', 'image2pipe',
                          '-vcodec', 'png', '-'], capture_output=True).stdout
    rows.append((t, dead_fraction(Image.open(io.BytesIO(png)).convert('RGB'))))
    t += step

flags, run = [], []
for t, f in rows + [(dur, 0.0)]:
    if f >= 1 / 3:
        run.append((t, f))
    else:
        if run and run[-1][0] - run[0][0] + step >= hold:
            a0, b0 = run[0][0], run[-1][0] + step
            if not any(lo <= a0 + 0.01 and b0 - 0.01 <= hi for lo, hi in ALLOW):
                flags.append((a0, b0, max(x[1] for x in run)))
        run = []
for a, b, f in flags:
    print(f'  {a:6.2f}–{b:5.2f} s  up to {f * 100:3.0f}% of the frame dead')
print(f'{len(flags)} stretch(es) with ≥⅓ of the frame empty for ≥{hold:.1f} s' +
      (' — fill it: zoom the camera in, put footage/renders behind, scale the focal element (STYLE.md → Fill every frame)'
       if flags else ' — ok'))
sys.exit(1 if flags else 0)
