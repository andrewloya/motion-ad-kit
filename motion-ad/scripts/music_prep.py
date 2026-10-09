#!/usr/bin/env python3
"""Map a music track for a motion ad: where the bass comes in, the breaks, the biggest hits, the bars, the key, the words.
Every time it prints is MEASURED from the audio, never grid math. Read-only on your files.

usage: uv run --with numpy --with scipy python <skill>/scripts/music_prep.py <cmd> ...
  map    <audio> [--from S --to S] [--words W.json] [--ad-start S] [--hits N]
                                         the track's musical events (BASS IN, bass out / BREAK, SILENCE, the biggest
                                         hits) to hang story beats on, with the word sung at each (--words from `words`)
  bars   <audio> [--from S --to S] [--bpm N] [--ad-start S]
                                         per-bar low/mid/high energy: the track's shape (sparse intro vs full beat)
  key    <audio> [--from S --to S]      the key (Krumhansl), for sound-effect notes in key (mix.py "note")
  words  <audio> --from S --to S [--out W.json] [--ad-start S]
                                         free local Whisper (large-v3-turbo) → words with times, swears flagged.
                                         Also the way to check a voice-over or the final mix says what the script says.
  grid   <audio> [--from S --to S] [--ad-start S] [--out grid.json]
                                         the measured beat grid (needs: uv run --with librosa --with numpy --with scipy):
                                         bpm, beat 0, and every bar start in the window, for cuts and hits to snap to
  cut    <audio> --from S --to S --out window.wav
                                         cut the ad's window from the track (48 kHz wav), ready for stems / mix.py
All times are TRACK time; --ad-start (track time at ad 0) adds an ad-time column.
Check a render's cuts against the grid: scripts/beat_check.py. Stems: see PIPELINE.md §4 (demucs, free, local).
"""
import json, os, re, subprocess, sys, tempfile

SWEAR = re.compile(r"(fuck|shit|bitch|nigg|pussy|cunt|whore|slut|motherf|bastard)|^(ass|asses|dick|dicks|hoe|hoes|cock|damn|goddamn)$")


def load_words(words_json=None):
    return sorted(json.load(open(words_json)), key=lambda w: w['start']) if words_json else []


def cmd_grid(path, a0=None, a1=None, ad_start=None, out=None):
    import numpy as np
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True)
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    _, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, units='time', tightness=200)
    lo, hi = (a0 or 0) - 6, (a1 or 1e9) + 6
    b = beats[(beats > lo) & (beats < hi)]
    if len(b) < 12:
        b = beats
    ibi = np.median(np.diff(b))
    k = np.concatenate([[0], np.cumsum(np.maximum(1, np.round(np.diff(b) / ibi)))])
    for _ in range(3):                                   # fit a straight line, drop outliers, refit
        P, T0 = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, b, rcond=None)[0]
        res = b - (T0 + P * k)
        keep = np.abs(res) < max(0.04, 2.5 * np.sqrt((res ** 2).mean()))
        b, k = b[keep], k[keep]
    T0 = T0 - P * np.ceil(T0 / P)
    print(f"~{60 / P:.2f} bpm (fit rms {np.sqrt((res[keep] ** 2).mean()) * 1000:.0f} ms over {len(b)} beats). beat k = {T0:.4f} + {P:.5f}*k")
    print("Bars assume beat 0 is a downbeat: check one against `map`'s first BASS IN and shift by whole beats if not.")
    t0, t1 = (a0 or 0), (a1 or len(y) / sr)
    kk = int(np.ceil((t0 - T0) / P))
    print(f"{'track s':>8} {'ad s':>7}  beat")
    while T0 + P * kk <= t1:
        t = T0 + P * kk
        ad = f"{t - ad_start:7.3f}" if ad_start is not None else '      -'
        print(f"{t:8.3f} {ad}  {'BAR' if kk % 4 == 0 else '   '} {kk}")
        kk += 1
    if out:
        json.dump({'P': float(P), 'T0': float(T0), 'bpm': float(60 / P)}, open(out, 'w'))
        print(f'→ {out}')


def cmd_cut(path, a0, a1, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a0), '-t', str(a1 - a0), '-i', path, '-ar', '48000', out], check=True)
    print(f'{out}  ({a1 - a0:.2f} s from track {a0:.3f})')


def clean(t):
    return re.sub(r"[^a-z']", '', (t or '').lower()).strip("'")


def decode(path, sr):
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype('float64')


def envelopes(path, a0, a1, sr=22050, hop=441):
    import numpy as np
    from scipy.signal import butter, sosfiltfilt
    x = decode(path, sr)
    s0 = int((a0 or 0) * sr); s1 = int(a1 * sr) if a1 else len(x)
    x = x[s0:s1]
    def env(sig):
        n = len(sig) // hop
        f = sig[: n * hop].reshape(n, hop)
        v = np.sqrt((f * f).mean(1) + 1e-12)
        return 20 * np.log10(v / (np.percentile(v, 95) + 1e-12))
    band = lambda lo, hi: env(sosfiltfilt(butter(4, [lo, hi], 'band', fs=sr, output='sos'), x))
    return x, env, env(sosfiltfilt(butter(4, 150, 'low', fs=sr, output='sos'), x)), band(300, 2500), band(4000, 10000)


def cmd_map(path, a0=None, a1=None, words=(), ad_start=None, nhits=8):
    import numpy as np
    sr, hop = 22050, 441                                 # 20 ms frames
    x, env, low, _, _ = envelopes(path, a0, a1, sr, hop)
    present = low > -16
    # close tiny holes (<120 ms) so kick gaps don't read as breaks
    k = 0
    while k < len(present):
        if not present[k]:
            j = k
            while j < len(present) and not present[j]:
                j += 1
            if j - k < 6 and k > 0 and j < len(present):
                present[k:j] = True
            k = j
        else:
            k += 1
    # drop tiny bass blips (<260 ms) inside a gap so a break with one stray kick reads as one break
    k = 0
    while k < len(present):
        if present[k]:
            j = k
            while j < len(present) and present[j]:
                j += 1
            if j - k < 13 and k > 0 and j < len(present):
                present[k:j] = False
            k = j
        else:
            k += 1
    ev = []
    # dead-silence gaps (whole mix drops out ≥ 0.25 s) — the held breath before a big hit
    full_db = env(x)
    quiet = full_db < -35
    k = 0
    while k < len(quiet):
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - k) * hop / sr >= 0.25:
                ev.append((k, f"SILENCE {(j - k) * hop / sr:.2f}s  (hit after it = a hook exit)"))
            k = j
        else:
            k += 1
    for k in range(1, len(present)):
        if present[k] and not present[k - 1]:
            ev.append((k, 'BASS IN'))
        if not present[k] and present[k - 1]:
            j = k
            while j < len(present) and not present[j]:
                j += 1
            ev.append((k, f"bass out {((j - k) * hop / sr):.2f}s" + ('  ← BREAK' if (j - k) * hop / sr >= 0.8 else '')))
    # biggest broadband hits (spectral-flux-ish on the full signal); --hits N for a denser list
    full = env(x)
    flux = np.maximum(np.diff(full, prepend=full[0]), 0)
    hits = []
    for k in np.argsort(flux)[::-1][: 60 * nhits]:
        if all(abs(k - h) > 12 for h in hits):
            hits.append(int(k))
        if len(hits) == nhits:
            break
    for k in hits:
        ev.append((k, f"hit (+{flux[k]:.0f} dB)"))
    def word_at(t):
        for w in words:
            if w['start'] - 0.05 <= t <= w['end'] + 0.05:
                return w['text'] + ('  [muted]' if w.get('disabled') else '')
        return ''
    print(f"{'song s':>8} {'ad s':>7}  event")
    for k, name in sorted(ev):
        st = (a0 or 0) + k * hop / sr
        ad = f"{st - ad_start:7.3f}" if ad_start is not None else '      -'
        print(f"{st:8.3f} {ad}  {name:34} {word_at(st)}")
    print('\nHang beats on these (STRUCTURE.md → Map the track first). Times are measured, not grid: trust them over any bpm.'
          '\nWant the words sung at each event? run `words` first and pass --words. Sparse intro reading noisy? use `bars`.')


def cmd_bars(path, a0=None, a1=None, bpm=None, ad_start=None):
    """per-bar low / mid / high energy — the song's shape at a glance (sparse intros, where the full beat starts)."""
    import numpy as np
    sr, hop = 22050, 441
    x, env, low, mid, high = envelopes(path, a0, a1, sr, hop)
    if not bpm:                                          # tempo from the onset envelope's autocorrelation, 70–180 bpm
        on = np.maximum(np.diff(env(x), prepend=0), 0); on -= on.mean()
        ac = np.correlate(on, on, 'full')[len(on) - 1:]
        fps = sr / hop
        lags = np.arange(int(fps * 60 / 180), int(fps * 60 / 70))
        bpm = 60 * fps / lags[int(np.argmax(ac[lags]))]
    bar = 4 * 60 / bpm
    fr = lambda t: int(t * sr / hop)
    blocks = ' ▁▂▃▄▅▆▇█'
    def lvl(db):
        return blocks[int(np.clip((db + 30) / 30 * 8, 0, 8))]
    print(f"~{bpm:.1f} bpm, or {bpm * 2:.1f} / {bpm / 2:.1f} (half/double time is ambiguous; a stored bpm is often wrong) —"
          f" bar = {bar:.3f} s. Override with --bpm; bars start at --from, so set --from on a downbeat (a BASS IN from `map`).")
    print(f"{'song s':>8} {'ad s':>7}   low mid high")
    t = 0.0
    total = len(low) * hop / sr
    while t < total - 0.05:
        a, b = fr(t), max(fr(t) + 1, fr(min(t + bar, total)))
        vals = [float(np.mean(v[a:b])) for v in (low, mid, high)]
        st = (a0 or 0) + t
        ad = f"{st - ad_start:7.3f}" if ad_start is not None else '      -'
        print(f"{st:8.3f} {ad}   {lvl(vals[0])*3} {lvl(vals[1])*3} {lvl(vals[2])*3}")
        t += bar


def cmd_key(path, a0=None, a1=None):
    import numpy as np
    sr = 22050
    x = decode(path, sr)
    x = x[int((a0 or 0) * sr): int(a1 * sr) if a1 else len(x)]
    n = 8192
    chroma = np.zeros(12)
    for i in range(0, len(x) - n, n // 2):
        spec = np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n)))
        f = np.fft.rfftfreq(n, 1 / sr)
        m = (f > 55) & (f < 2000)
        pc = np.round(12 * np.log2(f[m] / 440.0) + 9).astype(int) % 12
        np.add.at(chroma, pc, spec[m] ** 2)
    maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    mnr = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    scores = [(np.corrcoef(chroma, np.roll(p, k))[0, 1], names[k] + q) for k in range(12) for p, q in ((maj, ' major'), (mnr, ' minor'))]
    scores.sort(reverse=True)
    print(f"{scores[0][1]}  (r={scores[0][0]:.2f}; next {scores[1][1]} r={scores[1][0]:.2f})")
    root = scores[0][1].split()[0]
    scale = [0, 2, 4, 5, 7, 9, 11] if 'major' in scores[0][1] else [0, 2, 3, 5, 7, 8, 10]
    r = names.index(root)
    print('notes in key for mix.py "note":', ' '.join(names[(r + s) % 12] + '5' for s in scale))


def cmd_words(path, a0, a1, out, ad_start=None):
    """free local Whisper (large-v3-turbo) on a section → words in TRACK time, swears flagged. Also checks a voice-over."""
    import shutil
    tmp = tempfile.mkdtemp()
    clip = os.path.join(tmp, 'section.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a0), '-t', str(a1 - a0), '-i', path, '-ac', '1', '-ar', '16000', clip], check=True)
    exe = shutil.which('whisper')
    cmd = [exe] if exe else ['uvx', '--from', 'openai-whisper', 'whisper']   # first run downloads the model (~1.6 GB)
    subprocess.run(cmd + [clip, '--model', 'large-v3-turbo', '--word_timestamps', 'True', '--output_format', 'json',
                    '--output_dir', tmp, '--language', 'en', '--fp16', 'False', '--verbose', 'False'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res = json.load(open(os.path.join(tmp, 'section.json')))
    words, lines = [], []
    for seg in res.get('segments', []):
        line = []
        for w in seg.get('words', []):
            t = w['word'].strip()
            line.append({'text': t, 'start': round(w['start'] + a0, 3), 'end': round(w['end'] + a0, 3),
                         'disabled': bool(SWEAR.search(clean(t)))})
        words += line
        if line:
            lines.append(line)
    json.dump(words, open(out, 'w'), indent=1)
    for line in lines:
        st = line[0]['start']
        ad = f" ad {st - ad_start:6.2f}" if ad_start is not None else ''
        print(f"song {st:7.2f}{ad}  " + ' '.join(('[' + x['text'] + ']') if x['disabled'] else x['text'] for x in line))
    print(f"\n{sum(w['disabled'] for w in words)} swear(s) flagged [bracketed] → {out}. Whisper can mishear: check names and swears by ear."
          '\nPass it to `map --words` to see which word is sung at each musical event.')


def opts_of(rest, defaults):
    o = dict(defaults)
    for i in range(0, len(rest) - 1, 2):
        o[rest[i]] = rest[i + 1]
    return o



if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or any(x in ('-h', '--help', 'help') for x in a):
        print(__doc__); sys.exit(0)
    c = a[0]
    f = lambda v: float(v) if v not in (None, '') else None
    if c == 'map':
        o = opts_of(a[2:], {'--from': None, '--to': None, '--words': None, '--ad-start': None, '--hits': '8'})
        cmd_map(a[1], f(o['--from']), f(o['--to']), load_words(o['--words']), f(o['--ad-start']), int(o['--hits']))
    elif c == 'bars':
        o = opts_of(a[2:], {'--from': None, '--to': None, '--bpm': None, '--ad-start': None})
        cmd_bars(a[1], f(o['--from']), f(o['--to']), f(o['--bpm']), f(o['--ad-start']))
    elif c == 'key':
        o = opts_of(a[2:], {'--from': None, '--to': None})
        cmd_key(a[1], f(o['--from']), f(o['--to']))
    elif c == 'words':
        o = opts_of(a[2:], {'--from': None, '--to': None, '--out': 'words.json', '--ad-start': None})
        cmd_words(a[1], f(o['--from']), f(o['--to']), o['--out'], f(o['--ad-start']))
    elif c == 'grid':
        o = opts_of(a[2:], {'--from': None, '--to': None, '--ad-start': None, '--out': None})
        cmd_grid(a[1], f(o['--from']), f(o['--to']), f(o['--ad-start']), o['--out'])
    elif c == 'cut':
        o = opts_of(a[2:], {'--from': '0', '--to': None, '--out': 'window.wav'})
        cmd_cut(a[1], f(o['--from']), f(o['--to']), o['--out'])
    else:
        print(__doc__); sys.exit(1)
