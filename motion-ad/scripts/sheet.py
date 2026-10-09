#!/usr/bin/env python3
"""Contact sheet: sheet.py <video> <out.jpg> <offset> <cols> <thumbW> T1 T2 ...  (T = ad time; frame at T-offset)"""
import subprocess, sys, io
from PIL import Image, ImageDraw
vid, out, off, cols, tw = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
ts = [float(t) for t in sys.argv[6:]]
ims = []
for T in ts:
    fr = max(0.0, T - off)
    png = b""
    for back in (0, 0.1, 0.25, 0.5):      # past the last video frame (audio can run longer) → step back a little
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, fr - back):.3f}", "-i", vid, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if png: break
    if not png:
        print(f"skipped T {T:.2f}: no frame there", file=sys.stderr); continue
    im = Image.open(io.BytesIO(png)).convert("RGB"); im.thumbnail((tw, 10000)); ims.append((T, im))
th = max(i.size[1] for _, i in ims); rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * (tw + 4), rows * (th + 22)), "black"); d = ImageDraw.Draw(S)
for n, (T, im) in enumerate(ims):
    x, y = (n % cols) * (tw + 4), (n // cols) * (th + 22)
    S.paste(im, (x, y + 20)); d.text((x + 4, y + 4), f"T {T:.2f}", fill=(255, 220, 0))
S.save(out, quality=88); print(out, S.size)
