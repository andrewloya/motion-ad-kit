#!/usr/bin/env bash
# Start a new motion ad.
# usage: bash ~/.claude/skills/motion-ad/scripts/new_ad.sh <slug>
# Creates <adsDir from brand.json>/<YYYY-MM-DD>-<slug>/ (override with ADS_DIR=…) with a BLANK composition
# (scripts/starter.html) filled with the brand's palette and fonts, a local GSAP, empty claims.md / decisions.md,
# and the folders the pipeline expects. Never a copy of an example ad: every ad designs its own scenes.
set -euo pipefail
slug="${1:?usage: new_ad.sh <slug>}"
SK="$(cd "$(dirname "$0")/.." && pwd)"
vals="$(python3 - "$SK" <<'PY'
import json, os, shlex, sys
sk = sys.argv[1]
sys.path.insert(0, os.path.join(sk, 'scripts')); import kit
b = kit.brand()
if b.get('_setup'):
    print('brand.json is still the template: run the first-time setup (SETUP.md) before making an ad', file=sys.stderr)
    sys.exit(1)
p, f = b.get('palette', {}), b.get('fonts', {})
def font(role, default):
    v = f.get(role) or default
    return v if os.path.isabs(os.path.expanduser(v)) else os.path.join(sk, v)
vals = {
  'ADS': kit.expand(b.get('adsDir') or '~/motion-ads'),
  'BUSINESS': b.get('business', 'ad'),
  'STAGE': p.get('stage', '#000000'), 'INK': p.get('ink', '#ffffff'), 'ACCENT': p.get('accent', '#ffffff'),
  'FLOOD': p.get('flood') or p.get('accent', '#ffffff'), 'GLOW': p.get('glow') or p.get('accent', '#ffffff'),
  'F_HEADLINE': font('headline', 'fonts/SpaceGrotesk-Variable.ttf'), 'F_ACCENT': font('accent', 'fonts/InstrumentSerif-Italic.ttf'),
  'F_MONO': font('mono', 'fonts/JetBrainsMono.ttf'), 'F_TITLES': font('titles', 'fonts/BebasNeue-Regular.ttf'),
  'F_HERO': font('hero', 'fonts/Archivo-VF.ttf'), 'LOGO': kit.expand(b.get('logo') or ''),
}
for k, v in vals.items():
    print(f'{k}={shlex.quote(str(v))}')
PY
)" || exit 1
eval "$vals"
DST="${ADS_DIR:-$ADS}/$(date +%F)-$slug"
[ -e "$DST" ] && { echo "exists: $DST" >&2; exit 1; }
mkdir -p "$DST"/{assets/audio,assets/footage,assets/vendor,assets/img,fonts,pipeline,renders,versions}
for f in "$F_HEADLINE" "$F_ACCENT" "$F_MONO" "$F_TITLES" "$F_HERO"; do
  [ -f "$f" ] || { echo "font not found: $f (brand.json → fonts)" >&2; exit 1; }
  cp -n "$f" "$DST/fonts/" 2>/dev/null || true
done
[ -n "$LOGO" ] && [ -f "$LOGO" ] && cp "$LOGO" "$DST/assets/img/"
cp "$SK/vendor/gsap.min.js" "$DST/assets/vendor/"
python3 - "$SK/scripts/starter.html" "$DST/index.html" <<PY
import sys, os
s = open(sys.argv[1]).read()
rep = {'__SLUG__': '$slug', '__BUSINESS__': """$BUSINESS""", '__STAGE__': '$STAGE', '__INK__': '$INK', '__ACCENT__': '$ACCENT',
       '__FLOOD__': '$FLOOD', '__GLOW__': '$GLOW', '__F_HEADLINE__': os.path.basename('$F_HEADLINE'),
       '__F_ACCENT__': os.path.basename('$F_ACCENT'), '__F_MONO__': os.path.basename('$F_MONO'),
       '__F_TITLES__': os.path.basename('$F_TITLES'), '__F_HERO__': os.path.basename('$F_HERO')}
for k, v in rep.items():
    s = s.replace(k, v)
open(sys.argv[2], 'w').write(s)
PY
cat > "$DST/claims.md" <<'MD'
# Claims: every number and offer word this ad shows or says (scripts/claims_check.py reads this)
| claim | source (where you checked it) | checked |
|---|---|---|
MD
cat > "$DST/decisions.md" <<'MD'
# Decisions: the owner's rulings for THIS ad (the critic reads this and never asks for what's ruled out)
-
## Words never shown
-
MD
printf 'renders/*-raw.mp4\nrenders/qa/\n' > "$DST/.gitignore"
echo "new ad: $DST"
echo "next: SKILL.md → Build order step 2: pick the track (a new one, see ads-log.md), add your (planned) row to"
echo "      ads-log.md, then map it: uv run --with numpy --with scipy python $SK/scripts/music_prep.py map <track>"
