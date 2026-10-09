"""Narration straight from ElevenLabs, with the same knobs as elevenlabs.io, including the v3/v4 stability
'creativity' setting (0.0 Creative · 0.5 Natural · 1.0 Robust). From the LYRC build: going direct instead of through
a reseller was "WAY better cuz u can adjust creativity".

uv run --with requests python <skill>/scripts/voice.py <narration.json> <outdir> [--voice <voice id>] [--model eleven_v4]
       [--stability 0.0] [--takes 3] [--only 01,02] [--tag c]
narration.json = [{"id": "01", "text": "one whole spoken sentence"}, ...]
Writes <outdir>/<id>-<tag><k>.wav (48 kHz mono) + .json word timings. The voice defaults to brand.json → voice.id.
ELEVENLABS_API_KEY from the environment or ~/.config/motion-ad/.env (never printed).
"""
import json, os, sys, base64, subprocess, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit

def opt(k, d):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

def key():
    return kit.env_key('ELEVENLABS_API_KEY')

script, out = sys.argv[1], sys.argv[2]
VOICE = opt('--voice', (kit.brand(script).get('voice') or {}).get('id') or 'cgSgspJ2msm6clMCkdW9')  # default: Jessica (premade)
model, stab, takes = opt('--model', 'eleven_v4'), float(opt('--stability', '0.0')), int(opt('--takes', '3'))
tag = opt('--tag', 'c'); only = set(filter(None, opt('--only', '').split(',')))
os.makedirs(out, exist_ok=True); K = key()
for ln in json.load(open(script)):
    if only and ln['id'] not in only: continue
    for k in range(1, takes + 1):
        body = {'text': ln['text'], 'model_id': model,
                'voice_settings': {'stability': stab, 'similarity_boost': 0.75, 'style': 0.0, 'use_speaker_boost': True}}
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128',
                          headers={'xi-api-key': K, 'Content-Type': 'application/json'}, json=body, timeout=180)
        if r.status_code != 200: print(ln['id'], k, 'HTTP', r.status_code, r.text[:200]); continue
        d = r.json(); base = os.path.join(out, f"{ln['id']}-{tag}{k}")
        open(base + '.mp3', 'wb').write(base64.b64decode(d['audio_base64']))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', base + '.mp3', '-ar', '48000', '-ac', '1', base + '.wav'], check=True)
        a = d.get('alignment') or {}
        chars, st, en = a.get('characters', []), a.get('character_start_times_seconds', []), a.get('character_end_times_seconds', [])
        words, cur, s0 = [], '', None
        for c, s, e in zip(chars, st, en):
            if c.isspace():
                if cur: words.append({'text': cur, 'start': round(s0, 3), 'end': round(pe, 3)}); cur = ''
                continue
            if not cur: s0 = s
            cur += c; pe = e
        if cur: words.append({'text': cur, 'start': round(s0, 3), 'end': round(pe, 3)})
        json.dump({'text': ln['text'], 'model': model, 'stability': stab, 'words': words}, open(base + '.json', 'w'), indent=1)
        json.dump(words, open(base + '.words.json', 'w'), indent=1)          # mix.py reads <wav>.words.json for --words-out
        dur = words[-1]['end'] - words[0]['start'] if len(words) > 1 else 0
        print(ln['id'], f'{tag}{k}', f"{words[-1]['end'] if words else 0:.2f}s", f"{len(words) / dur:.2f} words/s" if dur else '')
