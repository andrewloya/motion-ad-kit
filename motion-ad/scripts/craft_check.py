#!/usr/bin/env python3
"""Is there enough animation, and none of the machine-made tells? Reads the composition, not the render.

python3 <skill>/scripts/craft_check.py <ad folder or index.html> [--duration 30.5]
- animation density: tween call sites per second of ad. From the LYRC build: "not enough in animations".
  Calibrated on the LYRC ads: liked ones 5.4–7.2/s · rejected ones 2.4–3.8/s ("SUCKED").
  Bar ≥ 4/s. Add motion to the FEW things on screen (camera surges, per-letter moves, parallax layers, light sweeps,
  secondary motion on landings), not new things: pace_check still has to pass.
- yoyo pulses: 0 allowed (breathing / glow pulses; from the LYRC build: "we need to not do the pulsing to the beat").
- linear eases: 0 allowed (never-linear-motion rule; linear is the first thing that reads "vibe coded").
- negative timeline positions: 0 allowed. GSAP shifts the WHOLE timeline later to make room for a tween placed
  before 0, so every cue lands late (0.3 s off on the kit's demo ad).
- per-letter / staggered animation: at least one split word or staggered group (wrap()/.ch, letter spans, stagger:),
  so type moves like type.
It counts call sites, so a tween inside a loop counts once: the number is a floor.
Exit 1 when a bar fails. It can't see the LOOK: the vibe-coded tells in STYLE.md → Craft are judged by eye + critic.
"""
import re, sys, os
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
p = sys.argv[1]; p = os.path.join(p, 'index.html') if os.path.isdir(p) else p
src = open(p).read()
dur = float(sys.argv[sys.argv.index('--duration') + 1]) if '--duration' in sys.argv else None
if dur is None:
    m = re.search(r'data-composition-id="[^"]*"[^>]*data-duration="([\d.]+)"', src) or re.search(r'data-duration="([\d.]+)"', src)
    dur = float(m.group(1)) if m else 30.0
tweens = len(re.findall(r'\bft\(|\.fromTo\(|\.from\(|\.to\(|\bmoveScreen\(|\bpanelTo\(|\brise\(|\bflood\(|\bdiveTo\(|\bflip\(|\btypeOn\(|\bmblur\(', src))
linear = re.findall(r"ease\s*:\s*['\"](?:none|linear|power0[\w.]*)['\"]", src)
pulses = re.findall(r"yoyo\s*:\s*true", src)
negative = re.findall(r'\bft\(\s*-\d|\btl\.(?:to|from|fromTo|set)\([^;]*?,\s*-\d[\d.]*\s*\)', src)
perletter = bool(re.search(r'\bwrap\(|class="ch"|\.ch\b|class="l"|splitText|SplitText|stagger\s*:', src))
dens = tweens / dur
print(f'animation {tweens} tweens / {dur:.1f} s = {dens:.1f}/s (bar 4.0) · linear eases {len(linear)} (bar 0) · yoyo pulses {len(pulses)} (bar 0) · per-letter {"yes" if perletter else "NO"}')
fails = []
if dens < 4.0: fails.append('NOT ENOUGH ANIMATION: animate the few things on screen more (from the LYRC build: "not enough in animations")')
if linear: fails.append('LINEAR EASE: every move eased (never-linear-motion)')
if pulses: fails.append('PULSING: yoyo/repeat tweens pump in and out; use one long eased move (from the LYRC build: "not do the pulsing to the beat")')
if negative: fails.append(f'NEGATIVE TIME: {len(negative)} tween(s) placed before 0 shift the whole timeline late; start them at 0')
if not perletter: fails.append('NO PER-LETTER MOTION: split the hook\'s star word and move its letters')
print('\n'.join(fails) if fails else 'ok')
sys.exit(1 if fails else 0)
