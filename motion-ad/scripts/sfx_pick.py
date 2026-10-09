"""Find a real sound in the SFX library and cut it ready for mix.py.

  python3 scripts/sfx_pick.py find cartoon impact          # search the pro pack + generated sounds
  python3 scripts/sfx_pick.py cut "<file from find>" slab-slam --from 0.8 --dur 2.0 [--fade-in 0.05] [--fade-out 0.4]

`cut` writes <sfxDir>/cuts/<name>.wav (48 kHz, so mix.py never has to
resample a 96/192 kHz file, and it fixes WAVs libsndfile can't read) and prints the PEAK offset:
place the "sample" event at  t = (the frame the hit lands on) - peak.
Library: <sfxDir from brand.json>/packs/ (any folders of .wav/.aif/.mp3: e.g. the free Sonniss GDC bundle,
royalty-free, no attribution, never for AI/ML training; SETUP.md → Sounds) + sfx_gen.py outputs.
The pack is indexed by file and folder name on the first `find` (packs/index.json); delete that file after adding packs.
"""
import json, os, subprocess, sys, argparse, wave, struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
LIB = kit.expand(kit.brand().get('sfxDir') or '~/motion-ads/sfx-library')

def index_packs():
    p = os.path.join(LIB, 'packs', 'index.json')
    if os.path.exists(p):
        return json.load(open(p))
    rows = []
    for root, _, files in os.walk(os.path.join(LIB, 'packs')):
        for f in sorted(files):
            if f.lower().endswith(('.wav', '.aif', '.aiff', '.mp3', '.flac')):
                full = os.path.join(root, f)
                d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', full],
                                   capture_output=True, text=True).stdout.strip()
                rows.append({'name': os.path.splitext(f)[0], 'library': os.path.relpath(root, os.path.join(LIB, 'packs')),
                             'dur': float(d or 0), 'file': full})
    if rows:
        json.dump(rows, open(p, 'w'), indent=1)
    return rows

def find(words):
    os.makedirs(os.path.join(LIB, 'packs'), exist_ok=True)
    rows = index_packs()
    gen = os.path.join(LIB, 'index.json')                       # sfx_gen.py outputs: <name>-t<k>.wav
    if os.path.exists(gen):
        for k, v in json.load(open(gen)).items():
            for t in range(1, int(v.get('takes', 1)) + 1):
                rows.append({'name': f'{k} (generated): {v.get("prompt", "")}', 'library': 'sfx_gen',
                             'dur': v.get('dur', 0), 'file': os.path.join(LIB, f'{k}-t{t}.wav')})
    ws = [w.lower() for w in words]
    hits = [r for r in rows if all(w in (r['name'] + ' ' + r['library']).lower() for w in ws)]
    for r in hits:
        print(f"{r['dur']:6.2f}s  {r['library'][:40]:40s}  {r['name'][:70]}\n          {r['file']}")
    print(f'{len(hits)} match(es)' + ('' if hits else ' — try fewer words, or generate one: sfx_gen.py'))

def peak_offset(path):
    with wave.open(path) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw != 3: return None
    vals = [int.from_bytes(raw[i:i + 3], 'little', signed=True) for i in range(0, len(raw), 3)]
    mono = [abs(sum(vals[i:i + ch])) for i in range(0, len(vals), ch)]
    win = max(1, int(0.02 * sr)); best, at, acc = -1, 0, 0
    for i, v in enumerate(mono):
        acc += v
        if i >= win: acc -= mono[i - win]
        if acc > best: best, at = acc, i - win // 2
    return max(0, at) / sr

def cut(src, name, start, dur, fin, fout):
    os.makedirs(os.path.join(LIB, 'cuts'), exist_ok=True)
    out = os.path.join(LIB, 'cuts', f'{name}.wav')
    af = f'afade=t=in:d={fin},afade=t=out:st={max(0.0, dur - fout)}:d={fout},aresample=48000:filter_size=64'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', src, '-af', af,
                    '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', out], check=True)
    pk = peak_offset(out)
    print(f'{out}\npeak at {pk:.3f}s → place the "sample" event at t = hit - {pk:.3f}')

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('find', 'cut'): sys.exit(__doc__)
    if sys.argv[1] == 'find': find(sys.argv[2:])
    else:
        ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('name')
        ap.add_argument('--from', dest='start', type=float, default=0); ap.add_argument('--dur', type=float, required=True)
        ap.add_argument('--fade-in', type=float, default=0.01); ap.add_argument('--fade-out', type=float, default=0.3)
        a = ap.parse_args(sys.argv[2:]); cut(a.src, a.name, a.start, a.dur, a.fade_in, a.fade_out)
