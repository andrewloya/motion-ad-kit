#!/usr/bin/env python3
"""Instagram Reels UI mock (1080x1920 RGBA) for safe-zone checks, plus the safe-zone guides.

Yellow = organic Reels UI (caption/username/audio bottom-left, action rail right, nav bar).
Red dashed = Meta's Reels-ads guidance: keep ~14% top (270px), ~35% bottom (670px), 6% sides (65px) clear.
Run: uv run --with pillow python <skill>/scripts/ig_overlay.py <out.png> [--no-guides]            overlay only
     uv run --with pillow python <skill>/scripts/ig_overlay.py <out.jpg> --video <mp4> --at <sec>   overlay ON that frame
"""
import sys
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print(__doc__); sys.exit(0)
out = sys.argv[1]; guides = "--no-guides" not in sys.argv
_opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
VIDEO, AT = _opt("--video"), float(_opt("--at") or 0)
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
import os
_FONT = next((f for f in ("fonts/SpaceGrotesk-Variable.ttf",
              os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "example", "fonts", "SpaceGrotesk-Variable.ttf"))
              if os.path.exists(f)))
F = lambda s, w=600: ImageFont.truetype(_FONT, s)
# scrims IG draws for legibility
for y in range(0, 300):
    d.line([(0, y), (W, y)], fill=(0, 0, 0, int(110 * (1 - y / 300) ** 1.5)))
for y in range(1300, H):
    d.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * ((y - 1300) / (H - 1300)) ** 1.3)))
WH = (255, 255, 255, 255)
# top bar
d.text((44, 92), "Reels", font=F(54), fill=WH)
d.rounded_rectangle([968, 96, 1036, 150], 14, outline=WH, width=6); d.ellipse([987, 108, 1017, 138], outline=WH, width=6)
# right rail
x = 1000
def label(y, t): d.text((x, y), t, font=F(30), fill=WH, anchor="mt")
d.polygon([(x - 34, 1160), (x, 1200), (x + 34, 1160), (x + 34, 1140), (x + 18, 1126), (x, 1136), (x - 18, 1126), (x - 34, 1140)], outline=WH, width=6); label(1214, "1,204")
d.ellipse([x - 34, 1280, x + 34, 1344], outline=WH, width=6); label(1356, "86")
d.polygon([(x - 36, 1430), (x + 36, 1404), (x + 8, 1474)], outline=WH, width=6); label(1488, "31")
for k in (-20, 0, 20): d.ellipse([x + k - 5, 1565, x + k + 5, 1575], fill=WH)
d.rounded_rectangle([x - 32, 1640, x + 32, 1704], 10, outline=WH, width=5)
# bottom-left: who, caption, audio
d.ellipse([40, 1592, 104, 1656], outline=WH, width=4)
d.text((122, 1604), "yourhandle", font=F(34), fill=WH)
d.rounded_rectangle([290, 1598, 410, 1654], 12, outline=WH, width=3); d.text((350, 1626), "Follow", font=F(28), fill=WH, anchor="mm")
d.text((40, 1682), "a caption that runs two lines long so it covers… more", font=F(32), fill=WH)
d.text((40, 1736), "♫  artist · song (original audio)", font=F(28), fill=(235, 235, 235, 255))
# nav bar
d.rectangle([0, 1790, W, H], fill=(0, 0, 0, 235))
for i in range(5):
    cx = 108 + i * 216
    d.rounded_rectangle([cx - 28, 1832, cx + 28, 1880], 10, outline=WH, width=5)
if guides:
    RED, YEL = (255, 59, 74, 255), (255, 214, 0, 255)
    def dash(p0, p1, col, w=5, on=26, off=16):
        (x0, y0), (x1, y1) = p0, p1
        n = int(max(abs(x1 - x0), abs(y1 - y0)) // (on + off)) + 1
        for k in range(n):
            a = k * (on + off); b = min(a + on, max(abs(x1 - x0), abs(y1 - y0)))
            if x0 == x1: d.line([(x0, y0 + a), (x0, y0 + b)], fill=col, width=w)
            else: d.line([(x0 + a, y0), (x0 + b, y0)], fill=col, width=w)
    # ads safe area (Meta): 270 top, 670 bottom, 65 sides
    L, T, R, B = 65, 270, W - 65, H - 670
    dash((L, T), (R, T), RED); dash((L, B), (R, B), RED); dash((L, T), (L, B), RED); dash((R, T), (R, B), RED)
    d.text((L + 8, T + 8), "ADS SAFE AREA", font=F(26), fill=RED)
    # organic UI zones
    d.rectangle([944, 1100, 1062, 1720], outline=YEL, width=4)
    d.rectangle([28, 1580, 900, 1770], outline=YEL, width=4)
    d.rectangle([20, 70, 1060, 170], outline=YEL, width=4)
if VIDEO:
    import io, subprocess
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{AT:.3f}", "-i", VIDEO, "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    base = Image.open(io.BytesIO(png)).convert("RGBA").resize((W, H))
    im = Image.alpha_composite(base, im).convert("RGB")
im.save(out)
print("wrote", out)
