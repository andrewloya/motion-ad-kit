"""Shared helpers for the motion-ad scripts: where the skill lives, the business's brand.json, API keys.

brand.json is looked up in this order: $MOTION_AD_BRAND, a brand.json in the ad folder (or any folder above the file
a script was pointed at, or the current folder), then the skill's own brand.json. Keys come from the environment,
then ~/.config/motion-ad/.env (KEY=value lines). Keys are never printed.
"""
import json, os, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.expanduser('~/.config/motion-ad/.env')


def _walk_up(start):
    d = os.path.abspath(start if os.path.isdir(start) else os.path.dirname(start))
    while True:
        yield d
        parent = os.path.dirname(d)
        if parent == d:
            return
        d = parent


def brand_path(near=None):
    if os.environ.get('MOTION_AD_BRAND'):
        return os.path.expanduser(os.environ['MOTION_AD_BRAND'])
    for start in filter(None, [near, os.getcwd()]):
        for d in _walk_up(start):
            p = os.path.join(d, 'brand.json')
            if os.path.exists(p) and d != os.path.expanduser('~'):
                return p
    return os.path.join(SKILL, 'brand.json')


def brand(near=None):
    p = brand_path(near)
    try:
        return json.load(open(p))
    except FileNotFoundError:
        sys.exit(f'no brand.json at {p}: run the first-time setup (SETUP.md)')


def expand(p):
    return os.path.abspath(os.path.expanduser(p)) if p else p


def env_key(name, required=True):
    if os.environ.get(name):
        return os.environ[name]
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            line = line.strip()
            if line.startswith(name + '='):
                return line.split('=', 1)[1].strip().strip('"\'')
    if required:
        sys.exit(f'{name} not set: export it, or add {name}=... to {ENV_FILE} (SETUP.md → Keys)')
    return None


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
