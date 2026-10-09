#!/usr/bin/env python3
"""Make a REAL sound effect for one moment: ElevenLabs sound effects via fal.ai (~cents each), saved to the SFX library.

uv run python scripts/sfx_gen.py "<what you hear, specific>" <name> [--dur 1.5] [--takes 2]
  e.g. sfx_gen.py "aerosol spray paint can, three quick bursts, close mic" spray-3bursts --dur 1.2
Writes <sfxDir from brand.json>/<name>-t<k>.wav (48 kHz stereo) and logs the prompt in index.json.
Reuse before you generate: `sfx_gen.py --list`. Place a file with a mix.py "sample" event.
Why: the procedural whoosh/thump/pop/ticks in mix.py are placeholders. Spamming them (68 in 32 s) got
"wtf u doin w those sound effects lmao ur just spamming the same exact few" (from the LYRC build). Real sounds, fewer, each one
designed for its moment.
"""
import json, os, subprocess, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
LIB = kit.expand(kit.brand().get('sfxDir') or '~/motion-ads/sfx-library')
EP = 'https://fal.run/fal-ai/elevenlabs/sound-effects/v2'


def key():
    return kit.env_key('FAL_KEY')


def main():
    a = sys.argv[1:]
    os.makedirs(LIB, exist_ok=True)
    idx_p = os.path.join(LIB, 'index.json')
    idx = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); sys.exit(0)
    if a[0] == '--list':
        for name, v in sorted(idx.items()):
            print(f'{name:28s} {v["dur"]:>4}s  {v["prompt"]}')
        return
    prompt, name = a[0], a[1]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    dur, takes = float(opt('--dur', '1.5')), int(opt('--takes', '1'))
    k = key()
    for t in range(1, takes + 1):
        body = json.dumps({'text': prompt, 'duration_seconds': dur, 'prompt_influence': 0.5}).encode()
        req = urllib.request.Request(EP, data=body, headers={'Authorization': f'Key {k}', 'Content-Type': 'application/json'})
        url = json.load(urllib.request.urlopen(req, timeout=120))['audio']['url']
        mp3 = os.path.join(LIB, f'{name}-t{t}.mp3'); wav = mp3[:-4] + '.wav'
        urllib.request.urlretrieve(url, mp3)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ar', '48000', '-ac', '2', wav], check=True)
        os.remove(mp3)
        print(wav)
    idx[name] = {'prompt': prompt, 'dur': dur, 'takes': takes}
    json.dump(idx, open(idx_p, 'w'), indent=1)


if __name__ == '__main__':
    main()
