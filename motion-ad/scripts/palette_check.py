#!/usr/bin/env python3
"""Flag frames where colour outside the brand palette takes over (a red flood, a green stage, a purple wash).

uv run --with numpy --with pillow python <skill>/scripts/palette_check.py <video.mp4> [--step 0.25] [--limit 15]
       [--allow a-b,c-d] [--spread 22]
--allow: time ranges that are ONLY footage / product photos / real screens (their own colours are real content).
Allowed hues = every saturated colour in brand.json → palette (accent, flood, glow, extra) ± --spread degrees.
Black, white and greys are always fine. Counts saturated pixels whose hue is NOT allowed; a frame over --limit % is
flagged. Calibrated on the LYRC ads: approved frames peaked ~13% (warm sunrise footage, covers); a red tile board was
~18%, a red flood 90%. A flagged frame that is only footage / a product shot is fine: say so. A flood, stage, accent or
graphic in another hue is not. Exit 1 when anything is flagged, so it can gate a render.
From the LYRC build, after test hooks came out red and green: "why are they red? should be using proper colors".
"""
import colorsys, io, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
vid = sys.argv[1]
opt = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
step, limit = opt('--step', 0.25), opt('--limit', 15.0)
SPREAD = opt('--spread', 22.0)
_pal = kit.brand(vid).get('palette') or {}
HUES = []
for c in [_pal.get(k) for k in ('accent', 'flood', 'glow', 'stage', 'ink')] + list(_pal.get('extra') or []):
    if not c:
        continue
    r, g, b = (x / 255 for x in kit.hex_rgb(c))
    h, l, sat = colorsys.rgb_to_hls(r, g, b)
    if sat > 0.25 and 0.08 < l < 0.95:
        HUES.append(h * 360)
def allowed(h):
    if not HUES:
        return np.zeros_like(h, bool)
    return np.any([np.minimum(np.abs(h - x), 360 - np.abs(h - x)) <= SPREAD for x in HUES], axis=0)
ALLOW = [tuple(float(x) for x in r.split('-')) for r in (sys.argv[sys.argv.index('--allow') + 1].split(',') if '--allow' in sys.argv else [])]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid],
                           capture_output=True, text=True).stdout.strip())
bad = []
t = 0.0
while t < dur - 0.02:
    png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', '-vf', 'scale=270:-1',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    hsv = np.asarray(Image.open(io.BytesIO(png)).convert('RGB').convert('HSV')).astype(float)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    colored = (s > 0.45) & (v > 0.25)
    off = colored & ~allowed(h)
    pct = 100 * off.mean()
    if pct > limit and not any(lo <= t <= hi for lo, hi in ALLOW):
        hue = float(np.median(h[off]))
        name = 'red' if hue < 20 or hue >= 330 else 'orange/yellow' if hue < 70 else 'green' if hue < 170 else 'purple/pink'
        bad.append((t, pct, name))
    t += step
for t, pct, name in bad:
    print(f'  {t:6.2f} s  {pct:5.1f}% {name}')
print(f'{len(bad)} frame(s) over {limit:.0f}% off-palette' + (f' — the palette is black/white + brand hues {[round(x) for x in HUES]}° (STYLE.md → Colour)' if bad else ' — ok'))
sys.exit(1 if bad else 0)
