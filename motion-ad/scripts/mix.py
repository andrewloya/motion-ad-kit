#!/usr/bin/env python3
"""Mix a hook (or a whole ad): the track (or its stems) + real SFX from an event list (+ a narrator, the track ducked under it).

uv run --with numpy --with soundfile python <skill>/scripts/mix.py \
    --inst <track or no_vocals.wav | none> [--vocals <vocals.wav>] --stem-start <track s where that file begins> \
    --song-start <track s at ad 0> --dur <s> [--vocal-in <ad s>] [--vocal-out <ad s>] [--mute <song a-b,c-d>] \
    [--vocal-windows a-b,c-d] [--voice <narrator.wav> --voice-at <ad s> --duck 10] --events events.json --out assets/audio/premix-h1.wav
Voice/`file` paths in events.json resolve relative to events.json itself (e.g. "../assets/audio/vo/01-t1.wav").

events.json — one entry per move on screen, in AD time (every visual move gets a sound):
  [{"t": 0.00, "sfx": "whoosh", "dur": 0.55, "gain": 0.22},            # surge / camera move
   {"t": 0.52, "sfx": "thump",  "freq": 70, "gain": 0.55},             # stamp / slam / impact
   {"t": 0.95, "sfx": "ticks",  "n": 10, "gap": 0.03, "gain": 0.08},   # typing / letters landing
   {"t": 1.95, "sfx": "pop",    "note": "C6", "gain": 0.22},           # UI pop — pick notes IN THE SONG'S KEY
   {"t": 3.76, "sfx": "riser",  "dur": 0.45, "gain": 0.28},            # into the hook's exit
   {"t": 0.30, "sfx": "voice",  "file": "vo/01-c1.wav", "gain": 1.0},   # a narration line (voice.py); the track ducks under it
   {"t": 2.50, "sfx": "sample", "file": "~/…/sfx-library/spray-t1.wav", "gain": 0.35, "dur": 1.0}]   # a REAL sound (sfx_gen.py)
The procedural whoosh/thump/pop/ticks are placeholders: final cuts use "sample" sounds, few of them (STYLE.md → Sound).
A music-driven cut on the owner's track usually has NO sfx at all: events.json = [] (or voice events only).
--inst none = no music (a silent bed at 48 kHz): a voice-only cut.
Voice events duck the song by --duck dB while each line plays; with --words-out, every line's <file>.words.json is shifted
to ad time and written there (drive captions and scene changes from it).
Stems: `uvx --with numpy --with soundfile --from demucs demucs --two-stems=vocals -o <SP>/stems <window.wav>` (~10 s
for a 12 s window; cut the window first with ffmpeg and pass its start as --stem-start).
Writes FLOAT (a premix over 1.0 would clip as 16-bit). Then: ffmpeg -i premix.wav -af loudnorm=I=-13:TP=-1.0:LRA=9 -ar 48000 final.wav
"""
import argparse, json, os, sys
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--inst', required=True); ap.add_argument('--vocals'); ap.add_argument('--stem-start', type=float, required=True)
ap.add_argument('--song-start', type=float, required=True); ap.add_argument('--dur', type=float, required=True)
ap.add_argument('--vocal-in', type=float, default=0.0); ap.add_argument('--vocal-out', type=float)
ap.add_argument('--vocal-windows', default='', help='AD-time spans where the sung vocal plays, "a-b,c-d" (e.g. one sung line in a narration pause); overrides --vocal-in/out')
ap.add_argument('--vocal-fade', type=float, default=0.08, help='seconds each vocal window fades out over. A hard 80 ms stop mid-line sounds broken (from the LYRC build: "the audio cuts out weirdly at the end w the vocals"): end windows on a sung phrase end, or give 0.6+ here')
ap.add_argument('--mute', default='', help='song-time spans to mute in the vocal (swears), "a-b,c-d"')
ap.add_argument('--voice'); ap.add_argument('--voice-at', type=float, default=0.0); ap.add_argument('--duck', type=float, default=6.0)
ap.add_argument('--voice-gain', type=float, default=1.0)
ap.add_argument('--no-fade', action='store_true', help='keep a hit on frame 0 sharp (no 60 ms fade-in)')
ap.add_argument('--events'); ap.add_argument('--out', required=True); ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--words-out', help='write narration words in AD time (from voice events) to this JSON')
ap.add_argument('--fade-out', type=float, default=0.0, help='seconds of fade at the end')
a = ap.parse_args()

if a.inst == 'none':
    SR = 48000; inst = np.zeros((int((a.song_start - a.stem_start + a.dur) * SR) + 1, 2))
else:
    inst, SR = sf.read(a.inst, always_2d=True)
n = int(a.dur * SR); t = np.arange(n) / SR
i0 = int((a.song_start - a.stem_start) * SR)
if i0 < 0 or i0 + n > len(inst):
    sys.exit(f'stems cover song {a.stem_start:.2f}–{a.stem_start + len(inst) / SR:.2f}; the ad needs {a.song_start:.2f}–{a.song_start + a.dur:.2f}')
mix = inst[i0:i0 + n].copy()
if a.vocals:
    voc, sr2 = sf.read(a.vocals, always_2d=True); assert sr2 == SR
    v = voc[i0:i0 + n].copy()
    if a.vocal_windows:
        g = np.zeros(n)
        for span in a.vocal_windows.split(','):
            w0, w1 = (float(x) for x in span.split('-'))
            g = np.maximum(g, np.clip(np.minimum((t - w0 + 0.04) / 0.04, (w1 - t) / a.vocal_fade), 0, 1))
    else:
        g = np.clip((t - a.vocal_in + 0.04) / 0.04, 0, 1)                  # 40 ms fade in, landing on vocal-in
        if a.vocal_out is not None:
            g *= np.clip((a.vocal_out - t) / 0.08, 0, 1)                     # 80 ms bow-out
    for span in filter(None, a.mute.split(',')):
        s0, s1 = (float(x) - a.song_start for x in span.split('-'))
        g *= 1 - np.clip(np.minimum((t - s0 + 0.02) / 0.02, (s1 + 0.02 - t) / 0.02), 0, 1)
    mix += v * g[:, None]
if not a.no_fade:
    mix *= np.clip(t / 0.06, 0, 1)[:, None]                                # no click on frame 1 (--no-fade if 0 is a hit)

fx = np.zeros_like(mix)                                                     # SFX live apart from the song: voice ducks the song only
rng = np.random.default_rng(a.seed)
NOTES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
         'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
def hz(note):
    name, octv = note[:-1], int(note[-1]); return 440.0 * 2 ** ((NOTES[name] + 12 * (octv + 1) - 69) / 12)
def env(dur, att, dec):
    k = np.arange(int(dur * SR)) / SR
    return np.minimum(1, k / max(att, 1e-4)) * np.exp(-k / dec)
def whoosh(dur=0.3, lo=600, hi=5000, rev=False):
    x = rng.standard_normal(int(dur * SR)); f = np.linspace(lo, hi, len(x)) if rev else np.linspace(hi, lo, len(x))
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        c = np.exp(-2 * np.pi * f[i] / SR); s = (1 - c) * x[i] + c * s; y[i] = s
    y -= np.convolve(y, np.ones(20) / 20, 'same')
    e = np.sin(np.pi * np.linspace(0, 1, len(x))) ** (3 if rev else 1.5)
    return y * e / (np.abs(y).max() + 1e-9)
def pop(freq=880.0, dur=0.09):
    k = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * freq * k * (1 + 0.6 * np.exp(-k / 0.01))) * env(dur, 0.002, 0.025)
def thump(freq=55.0, dur=0.4):
    k = np.arange(int(dur * SR)) / SR; f = freq * (1 + 2.5 * np.exp(-k / 0.03))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(dur, 0.003, 0.12)
def tick(dur=0.025):
    return rng.standard_normal(int(dur * SR)) * env(dur, 0.0005, 0.004)
def place(sig, at, gain):
    i = int(at * SR)
    if i >= n or i + len(sig) <= 0:
        return
    s0 = max(0, -i); j = min(n, i + len(sig)); fx[max(i, 0):j] += (sig[s0: j - i] * gain)[:, None]

voice_spans, voice_words = [], []
EV = json.load(open(a.events)) if a.events else []
EVDIR = os.path.dirname(os.path.abspath(a.events)) if a.events else '.'
for e in EV:
    k, at, g = e['sfx'], float(e['t']), float(e.get('gain', 0.2))
    if k == 'voice':
        f = e['file'] if os.path.isabs(e['file']) else os.path.join(EVDIR, e['file'])
        vo, sr4 = sf.read(f, always_2d=True)
        if sr4 != SR:                                                   # voice.py writes 48 kHz; tracks are often 44.1
            vo = np.interp(np.arange(int(len(vo) * SR / sr4)) * sr4 / SR, np.arange(len(vo)), vo[:, 0])[:, None]
        voice_spans.append((at, at + len(vo) / SR, np.repeat(vo[:, :1], mix.shape[1], axis=1) * float(e.get('gain', 1.0))))
        wf = os.path.splitext(f)[0] + '.words.json'
        if os.path.exists(wf):
            ws = json.load(open(wf))
            for k, w in enumerate(ws):
                end = w['end']
                voice_words.append({'text': w['text'], 'start': round(w['start'] + at, 3), 'end': round(max(w['start'] + 0.05, end) + at, 3)})
        continue
    if k == 'sample':                                                    # a REAL sound file (sfx_pick.py cut / sfx_gen.py)
        f = os.path.expanduser(e['file']); f = f if os.path.isabs(f) else os.path.join(EVDIR, f)
        smp, sr5 = sf.read(f, always_2d=True)
        smp = smp.mean(axis=1)
        if sr5 != SR:
            smp = np.interp(np.arange(int(len(smp) * SR / sr5)) * sr5 / SR, np.arange(len(smp)), smp)
        if 'dur' in e:
            m = int(float(e['dur']) * SR); smp = smp[:m] * np.clip((m - np.arange(min(m, len(smp)))) / (0.03 * SR), 0, 1)
        place(smp / (np.abs(smp).max() + 1e-9), at, g)
        continue
    freq = hz(e['note']) if 'note' in e else e.get('freq')
    if k == 'whoosh':
        place(whoosh(e.get('dur', 0.3), e.get('lo', 600), e.get('hi', 5000)), at, g)
    elif k == 'riser':
        d = e.get('dur', 0.45); place(whoosh(d, e.get('lo', 300), e.get('hi', 5000), rev=True), at - d, g)   # ends ON t
    elif k == 'thump':
        place(thump(freq or 55, e.get('dur', 0.4)), at, g)
    elif k == 'pop':
        place(pop(freq or 880, e.get('dur', 0.09)), at, g)
    elif k == 'tick':
        place(tick(), at, g)
    elif k == 'ticks':
        for m in range(int(e.get('n', 5))):
            place(tick(), at + m * float(e.get('gap', 0.05)), g)
    else:
        sys.exit(f'unknown sfx {k!r} (sample, voice; placeholders: whoosh, riser, thump, pop, tick, ticks)')

if voice_spans:
    duck = np.ones(n)
    for s0, s1, _ in voice_spans:
        duck[max(0, int((s0 - 0.05) * SR)):min(n, int((s1 + 0.1) * SR))] = 10 ** (-a.duck / 20)
    duck = np.convolve(duck, np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same')             # 120 ms ramps
    mix *= duck[:, None]                                                    # the song bed only, not the SFX
    talking = np.zeros(n, bool)
    for s0, s1, vo in voice_spans:
        i = int(s0 * SR); j = min(n, i + len(vo)); fx[i:j] += vo[: j - i]
        talking[i:j] = True
    edges = np.flatnonzero(np.diff(np.r_[0, talking.astype(int), 0]))
    gaps = [(edges[k + 1] - edges[k]) / SR for k in range(1, len(edges) - 1, 2)]
    print(f'voice over {100 * talking.mean():.0f}% of the ad (aim 75–90%); longest gap between lines {max(gaps, default=0):.2f} s')
    if a.words_out:
        json.dump(sorted(voice_words, key=lambda w: w['start']), open(a.words_out, 'w'), indent=1)
        print(f'narration words in ad time → {a.words_out}')
if a.voice:
    vo, sr3 = sf.read(a.voice, always_2d=True)
    if sr3 != SR:
        sys.exit(f'resample the voice to {SR} Hz first (ffmpeg -ar {SR})')
    i = int(a.voice_at * SR); j = min(n, i + len(vo)); vo = vo[: j - i]
    if vo.shape[1] != mix.shape[1]:
        vo = np.repeat(vo[:, :1], mix.shape[1], axis=1)
    duck = np.ones(n); duck[i:j] = 10 ** (-a.duck / 20)
    duck = np.convolve(duck, np.ones(int(0.08 * SR)) / int(0.08 * SR), 'same')             # 80 ms ramps
    mix *= duck[:, None]; mix[i:j] += vo * a.voice_gain

mix = mix + fx
if a.fade_out > 0:
    mix *= np.clip((a.dur - t) / a.fade_out, 0, 1)[:, None]
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
sf.write(a.out, mix, SR, subtype='FLOAT')
print(f'wrote {a.out}  {a.dur:.2f} s  peak {np.abs(mix).max():.2f}  → loudnorm to -13 LUFS next')
