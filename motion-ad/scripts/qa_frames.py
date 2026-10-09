#!/usr/bin/env python3
"""Catch, on the RENDER, the things the owner catches by eye (in the LYRC build: the worse-song ad, rounds 2-7):

  POP        a part of the frame that exists for ONE frame (a screen showing a frame early, then gone)
             ("right after 20 a day it glitches for a frame or two and shows the add your audio track")  -> CHECK
  EDGE-CUT   readable text sliced by the frame edge ("DROP A V", "e a YouTube link")
             ("fix the framing on the youtube clip extraction ones")                                       -> CHECK
  TOP-PARKED big words sitting in the top 28% of the frame for ≥0.75 s
             ("the words at the top are never a good idea we dont wanna leave weird empty space")         -> CHECK

uv run --with numpy --with opencv-python-headless --with ocrmac python <skill>/scripts/qa_frames.py <render.mp4> [--out qa.json] [--step 0.25]
       [--skip-until <hook end s>] [--strips <dir>]

Nothing here is automatically wrong: a hook's impact frame is a one-frame pop on purpose, a designed element may bleed
letters off-frame, a wall of tiles runs past the edge. So every item is listed with its time, and --strips writes a
frame-by-frame strip (12 frames) around each POP and a full-size frame for each EDGE-CUT / TOP-PARKED, which
critic.sh hands to the critic. The 0.5 s contact sheet can never show a one-frame glitch; these strips can.
The hook (before --skip-until) is skipped for POP and TOP-PARKED: its impact frames and its title-over-picture
layout are by design. Measured on the worse-song ad: v3 lists its real glitch (8.5–8.9 s), v6 (approved) lists none there.
OCR = Apple Vision (ocrmac); text in boxes, so stylised display type reads fine.
"""
import json, os, subprocess, sys, tempfile, glob
import numpy as np

def opt(k, d): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'): sys.exit(__doc__)
VID = sys.argv[1]; STEP = float(opt('--step', '0.25'))
OUT = opt('--out', os.path.join(os.path.dirname(os.path.abspath(VID)), 'qa_frames.json'))
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
    'stream=width,height,r_frame_rate:format=duration', '-of', 'json', VID], capture_output=True, text=True).stdout)
W, H = probe['streams'][0]['width'], probe['streams'][0]['height']
num, den = probe['streams'][0]['r_frame_rate'].split('/'); FPS = float(num) / float(den)
DUR = float(probe['format']['duration'])

# ---- FLASH: every frame, small and grey
w, h = 90, 160
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', VID, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
# A pop is LOCAL: one part of the frame exists for exactly one frame while the camera may move everywhere else
# (v3: the "ADD YOUR AUDIO TRACK" box showed for one frame mid-dive). Footage and lyric renders change in steady
# steps, so a tile counts only when the frames on each side are themselves steady there.
SKIP = float(opt('--skip-until', '0'))
T = 10
tiles = fr[:, :h // T * T, :w // T * T].reshape(len(fr), h // T, T, w // T, T).mean(axis=(2, 4))
cand = []
for i in range(2, len(fr) - 2):
    if i / FPS < SKIP: continue
    din = np.abs(tiles[i] - tiles[i - 1]); dout = np.abs(tiles[i + 1] - tiles[i]); skip = np.abs(tiles[i + 1] - tiles[i - 1])
    m = np.minimum(din, dout)
    pop = (m > 14) & (skip < 0.35 * m) & (np.abs(tiles[i - 1] - tiles[i - 2]) < 0.5 * m) & (np.abs(tiles[i + 2] - tiles[i + 1]) < 0.5 * m)
    if pop.sum() >= 5: cand.append((round(i / FPS, 3), int(pop.sum())))
fl_spans = []
for t, sc in cand:
    if fl_spans and t - fl_spans[-1][1] < 0.15: fl_spans[-1][1] = t; fl_spans[-1][2] = max(fl_spans[-1][2], sc)
    else: fl_spans.append([t, t, sc])
fl_spans = sorted(sorted(fl_spans, key=lambda x: -x[2])[:8])

# ---- OCR checks on frames every STEP seconds
try:
    from ocrmac import ocrmac          # Apple Vision: macOS only
except ImportError:
    ocrmac = None
    print('note: no ocrmac (macOS only): EDGE-CUT and TOP-PARKED were skipped; check those by eye on the sheets')
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', VID, '-vf', f'fps=1/{STEP},scale=540:-1', os.path.join(tmp, 'f_%05d.png')], check=True)
edge, top = [], []
for k, f in enumerate(sorted(glob.glob(os.path.join(tmp, 'f_*.png'))) if ocrmac else []):
    t = round(k * STEP, 2)
    try: res = ocrmac.OCR(f, recognition_level='accurate').recognize()
    except Exception: continue
    for text, conf, (x, y, bw, bh) in res:                 # Vision boxes: normalised, origin bottom-left
        letters = sum(c.isalpha() for c in text)
        if conf < 0.5 or letters < 3: continue
        ytop = 1 - (y + bh)
        uiish = (' ' in text.strip() and letters >= 5) or bh >= 0.03   # a label/sentence, or big type; not a tile's lyric scrap
        if uiish and (x <= 0.006 or x + bw >= 0.994 or ytop <= 0.004 or y <= 0.004):
            side = 'left' if x <= 0.006 else 'right' if x + bw >= 0.994 else 'top' if ytop <= 0.004 else 'bottom'
            edge.append((t, side, text.strip()[:40]))
        if t >= SKIP and bh >= 0.035 and (ytop + bh / 2) < 0.28 and '@' not in text:   # an account header is UI, not parked words
            top.append((t, text.strip()[:30]))

def spans(items, key):
    out = []
    for it in items:
        t = it[0]
        if out and t - out[-1]['end'] <= STEP + 1e-6 and key(it) == out[-1]['key']:
            out[-1]['end'] = t; out[-1]['texts'].add(it[-1])
        else:
            out.append({'start': t, 'end': t, 'key': key(it), 'texts': {it[-1]}})
    return out
edge_sp = [sp for side in ('left', 'right', 'top', 'bottom')
           for sp in spans(sorted(e for e in edge if e[1] == side), key=lambda it: it[1])
           if sp['end'] - sp['start'] >= STEP - 1e-6]               # held ≥2 samples: not a word sliding past
edge_sp.sort(key=lambda sp: sp['start'])
top_sp = [s for s in spans(sorted(top), key=lambda it: 'top') if s['end'] - s['start'] + STEP >= 0.75]
report = {
    'pop': [{'start': a, 'end': b, 'tiles': sc} for a, b, sc in fl_spans],
    'edge_cut': [{'start': s['start'], 'end': s['end'], 'side': s['key'], 'text': sorted(s['texts'])[:4]} for s in edge_sp],
    'top_parked': [{'start': s['start'], 'end': s['end'], 'text': sorted(s['texts'])[:4]} for s in top_sp],
}
json.dump(report, open(OUT, 'w'), indent=1)
print(f'{os.path.basename(VID)}: {len(fr)} frames, OCR every {STEP}s')
for s in report['pop']: print(f"POP        {s['start']:.2f}-{s['end']:.2f}s  {s['tiles']} tiles exist for one frame: look at the strip; a glitch unless it's a designed hit")
for s in report['edge_cut']: print(f"EDGE-CUT   {s['start']:.2f}-{s['end']:.2f}s  {s['side']:6s} {' | '.join(s['text'])}")
for s in report['top_parked']: print(f"TOP-PARKED {s['start']:.2f}-{s['end']:.2f}s  {' | '.join(s['text'])}")
print(f"→ {OUT}")
STRIPS = opt('--strips', '')
if STRIPS:
    os.makedirs(STRIPS, exist_ok=True); made = []
    for s in report['pop']:
        t0 = max(0, s['start'] - 6 / FPS); o = os.path.join(STRIPS, f"pop-{s['start']:.2f}.jpg")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-i', VID, '-frames:v', '12', '-vf', 'scale=160:-1,tile=12x1', o]); made.append(o)
    for kind in ('edge_cut', 'top_parked'):
        for s in report[kind]:
            t = (s['start'] + s['end']) / 2; o = os.path.join(STRIPS, f"{kind}-{t:.2f}.jpg")
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', VID, '-frames:v', '1', '-vf', 'scale=720:-1', o]); made.append(o)
    report['images'] = made; json.dump(report, open(OUT, 'w'), indent=1)
    print(f"{len(made)} images → {STRIPS}")
print('check the listed frames' if fl_spans or edge_sp or top_sp else 'ok')
sys.exit(0)
