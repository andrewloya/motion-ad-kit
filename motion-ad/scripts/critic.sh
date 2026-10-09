#!/usr/bin/env bash
# A harsh, fresh-eyes review of a built ad BEFORE the owner sees it (SKILL.md → The owner's eye).
# usage: bash ~/.claude/skills/motion-ad/scripts/critic.sh <ad folder> [render.mp4]
# Reads the whole-ad + hook sheets, the script/narration, the composition, the owner's verdicts on past ads (ads-log),
# BRAND.md, and writes <ad folder>/renders/critic.md. Read-only; ~2–5 min. Fix what it finds, then run it again.
# Runs a fresh `claude -p` (Claude Code's headless mode). CRITIC_MODEL=<model id> picks the model (default: your default).
set -euo pipefail
AD="${1:?usage: critic.sh <ad folder> [render.mp4]}"; AD="$(cd "$AD" && pwd)"
VID="${2:-$(ls -t "$AD"/renders/*.mp4 2>/dev/null | grep -v -- '-raw' | head -1)}"
case "$VID" in /*) ;; *) [ -f "$VID" ] || VID="$AD/$VID" ;; esac
SK="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$VID" ] || { echo "no render in $AD/renders" >&2; exit 1; }
SHEET="$AD/renders/critic-sheet.jpg"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
last=$(python3 -c "print(max(0, float('$dur') - 0.1))")               # never sample exactly at the end (no frame there)
uv run -q --with pillow python "$SK/scripts/sheet.py" "$VID" "$SHEET" 0 8 240 $(seq 0 0.5 "$last") >/dev/null
# measured facts, so the critic doesn't guess pace / emptiness / colour from a contact sheet
MEAS=""
for c in pace_check pulse_check fill_check palette_check; do
  f="$SK/scripts/$c.py"; [ -f "$f" ] || continue
  extra=""
  if [ "$c" = pace_check ]; then
    if python3 -c "import sys; sys.exit(0 if float('$dur') <= 6 else 1)"; then extra="--hook"
    elif [ -n "$(ls "$AD"/pipeline/narration*.json 2>/dev/null)" ]; then extra="--narrated"; fi
    [ -s "$AD/pipeline/pace-allow" ] && extra="$extra --allow $(tr -d ' \n' < "$AD/pipeline/pace-allow")"   # the payoff range decisions.md allows
  fi
  MEAS+="$c: $( (uv run -q --with numpy --with pillow --with opencv-python-headless python "$f" "$VID" $extra 2>&1 || true) | tail -3 | tr '\n' ' ')
"
done
MEAS+="craft_check: $( (python3 "$SK/scripts/craft_check.py" "$AD" --duration "$dur" 2>&1 || true) | tr '\n' ' ')
"
# what the LYRC build kept catching by eye: one-frame pops, text cut by the frame edge, words parked at the top. The 0.5 s
# sheet can't show these, so qa_frames makes a strip / full frame for each, and the critic looks at them.
HOOK_END=$(python3 - "$AD" <<'PY' 2>/dev/null || echo 0
import json, glob, os, sys
fs = sorted(glob.glob(os.path.join(sys.argv[1], 'pipeline', 'words-ad*.json')), key=os.path.getmtime)
w = json.load(open(fs[-1])) if fs else []
end = next((x['end'] for x in w if x['text'].rstrip()[-1:] in '.?!'), 0)   # the hook = the first spoken sentence
print(round(end + 0.3, 2))
PY
)
QA_DIR="$AD/renders/qa"; rm -rf "$QA_DIR"
MEAS+="qa_frames (hook ends ~${HOOK_END}s): $( (uv run -q --with numpy --with opencv-python-headless --with ocrmac python "$SK/scripts/qa_frames.py" "$VID" --skip-until "$HOOK_END" --strips "$QA_DIR" --out "$AD/renders/qa_frames.json" 2>&1 || true) | grep -E '^(POP|EDGE|TOP)' | tr '\n' ';')
"
MEAS+="claims_check: $( (python3 "$SK/scripts/claims_check.py" "$AD" 2>&1 || true) | grep -E 'TRUE|says|FAIL|GATE|^ok' | tr '\n' ';')
"
QA_IMGS="$(ls "$QA_DIR"/*.jpg 2>/dev/null | tr '\n' ' ')"
# full-size frames: craft (vibe-coded or not) can't be judged from a 240 px sheet
FULL=""
# plus 0.4 s after each spoken line starts, so claims ("tap book", "add to cart") are judged at full size
CLAIMS=$(python3 - "$AD" "$dur" <<'PY' 2>/dev/null || true
import json, glob, os, sys
fs = sorted(glob.glob(os.path.join(sys.argv[1], 'pipeline', 'words-ad*.json')), key=os.path.getmtime)
if fs:
    w = json.load(open(fs[-1])); d = float(sys.argv[2]); out = []
    for i, x in enumerate(w):
        if x['start'] > 4 and (i == 0 or w[i - 1]['text'].rstrip()[-1:] in '.?!,' ) and x['start'] + 0.4 < d:
            out.append(f"{x['start'] + 0.4:.1f}")
    print(' '.join(out[:10]))
PY
)
for t in 0.5 1.5 2.5 3.5 $CLAIMS $(python3 -c "d=float('$dur'); print(f'{d-1.0:.1f}')"); do
  o="$AD/renders/critic-full-$t.jpg"; ffmpeg -v error -y -ss "$t" -i "$VID" -frames:v 1 -vf scale=720:-1 "$o" && FULL+="$o "
done
# the bar (CRITIC_NO_BAR=1 leaves it out: used to test the critic on old versions of the bar ad itself)
BAR_Q0=""
[ "${CRITIC_NO_BAR:-0}" = 1 ] || BAR_Q0='0. THE BAR for a whole ad is '"$SK"'/examples/worse-song/ (made for LYRC, a lyric-video app; from its build:
   "thats fucking gorgeous… the ideal motion graphic video we want to strive for"). Look at its sheet.jpg and read its
   README (the rounds of notes). Judge THIS ad against its craft, not its subject: is the hook as alive? Does the body pay
   the hook off with the real product as clearly? Is it as clean, as true and as readable? Name any note this ad repeats.'
read -r -d '' PROMPT <<EOF || true
You are the owner's harshest critic. The owner runs the business in $SK/BRAND.md (read it first: what they sell, who
buys, the voice, the never-print list). They judge these Instagram motion ads in seconds, on taste and on whether the
video actually proves its point. Their past verdicts are in $SK/ads-log.md (the Status column) and $SK/hooks-log.md.
The rules in the skill files below were earned by the original LYRC build's notes plus the owner's own; quotes marked
"from the LYRC build" show the taste bar. If $AD/decisions.md exists, it holds the owner's rulings for THIS ad (things
they banned or chose): never ask for anything it rules out. Judge ONLY this render, fresh (use critic-sheet.jpg and sheets named after this render;
line timings come from $AD/pipeline/words-ad.json, not transcript chunk starts): ignore any critic*.md files in the folder (earlier rounds). When a number anywhere
disagrees with the ad's claims.md (verified today), the verified one wins. The 0.5 s
sheet misses fast actions (a drag, a flash); if a claim's proof might be one, say "check at <t>" instead of MISSING.
Then study this ad:
- the whole-ad frame sheet (every 0.5 s): $SHEET
- full-size frames (hook at 0.5/1.5/2.5/3.5 s, 0.4 s after each spoken line starts, and the end card): $FULL
- qa_frames strips (pop-*.jpg = 12 consecutive frames around a one-frame pop; edge_cut-*/top_parked-* = a full frame): $QA_IMGS
- the hook sheet named after this render (e.g. hook-sheet-v7.jpg for ad-v7.mp4); skip sheets from other versions
- MEASURED on this render (facts, not guesses; they run without the ad's --allow ranges, so a flagged payoff or
  footage range may be allowed on purpose, and decisions.md says so if it is; pace_check already applies pipeline/pace-allow):
$MEAS
- the script / narration: the NEWEST $AD/pipeline/narration*.json and words-ad*.json (versioned names like -v6 exist), and the text in $AD/index.html
- the rules it should follow: $SK/SKILL.md (Non-negotiables, The owner's eye), $SK/HOOKS.md, $SK/STRUCTURE.md, $SK/STYLE.md, $SK/NARRATION.md, $SK/BRAND.md
Answer, citing frame times from the sheet:
1. Is the premise TRUE on screen? (e.g. "they all look different" while the outputs look the same = fail)
2. Every claim the voice/text makes: is its proof on screen at that moment? List each claim → proof or MISSING.
$BAR_Q0
3. Is the real flow from the customer's input shown when the subject needs it (what they bring or do → what the business does → what they get)?
4. Does any mock UI look fake, or cover the product's output?
5. Every stretch over ~3 s with no new information or real screen (filler).
6. The hook is the most engaging part of the video (from the LYRC build: "otherwise they will scroll and the rest of the
   video doesn't matter"). Look at $SK/examples/story-hooks/*/hook-sheet.jpg (the "insanely better… fire" bar): does THIS
   hook act out its line's story (characters, action, a twist, words that do what they say) at least that well? Fast is
   right in a hook; don't ask a hook to be calmer, only readable.
6a. The hook, WORDS FIRST: can a stranger finish "watching this gets me ___" after ~1 s (clear value)? Is the how
   withheld (open loop)? Vague / needs context / clever-but-unclear = "confusion = scroll" = fail, however good it looks.
   Then: stranger test, does it look real, is frame 0 a cover, does it fill the frame, does it carry designed type,
   and is the picture SURPRISING (not the literal illustration of the line — that's "boring predictable visuals")?
6b. Text: any subtitle strip / band / text slapped over the top = fail. Are there ~4–6 emphasis words designed INTO
   the scene (object, depth, full-frame beat, interaction)? Zero emphasis text is also a miss.
6e. Craft, on the FULL-SIZE frames: does it look made by a motion designer, or like an AI built a web page ("vibe
   coded")? Name every tell you see from $SK/STYLE.md → Craft (web card on a blurred photo, boxes or
   chips around words, >2 type voices in a frame, flat unlit vector, fade-ups, things that arrive and sit still). Is
   there enough animation (craft_check's density), with the few things on screen always moving? Does anything pulse
   to the beat (camera bumps, pushes on hits, breathing, glow pulses)? "we need to not do the pulsing to the beat".
6d. Phone readability: at 1080×1920 shown ~400 px wide on a phone, can every product UI beat be READ while it holds?
   Tiny UI (a whole editor, a thin waveform) = fail; name the crop that fixes it.
6c. Pace: count the scenes and the new elements per scene. Too fast / too much going on? Name what
   to CUT (whole beats), not what to speed up. Where does a key visual not get 2–3 s to land?
7. Anything else the owner has rejected before (ads-log Status, decisions.md), off-brand colours (BRAND.md), captions,
   empty frames, the same track/footage as a past ad…
8. THE OWNER'S EYE: the things caught in seconds (every one came from the notes on the ad that became the bar). Go
   through each, citing times; full-size frames and the qa_frames strips, not the 240 px sheet:
   a. CHARACTERS read in one look: solid silhouettes with faces and eyes, never see-through overlapping outlines
      ("the fucking thing is translucent cant tell whats going on… theres no eyes on the dude").
   b. EVERY WORD LEGIBLE in every frame at phone size: letters never overlap each other, a character's neck/body,
      or busy texture ("dont have the WORSE be too hard to read"; "letters… not overlapping their necks").
   c. NOT JUMBLED: few layers, each clear; calm dark backgrounds behind type; story moments slow enough to read, no
      fast cutting just to be fast ("blow up idea is good but it just looks super fuckin jumbled").
   d. CLAIMS ACTED OUT, not a number laid on a still ("they posted it 20x/day should be better. so bare").
   e. NO WORDS PARKED AT THE TOP, no dead bands, no half-empty frames ("the words at the top are never a good idea
      we dont wanna leave weird empty space"). See qa_frames TOP-PARKED.
   f. UI CROPS FRAMED like a camera: centred, nothing cut by the frame edge ("fix the framing"). See EDGE-CUT.
   g. NO ONE-FRAME POPS at hand-offs: look at every pop-*.jpg strip; a screen showing for a frame before its
      transition is a glitch ("it glitches for a frame or two"). A designed impact frame in the hook is fine.
   h. PROOF MATCHES THE LINE BEFORE IT: after "paste a link", the result comes from that link, not from something
      else. Real product data on screen (real screens, real numbers, appearing continuously), obvious typos fixed.
   i. NO DEAD TIME: no hold where nothing new happens, no gap over ~0.8 s between spoken lines ("too much time on the
      didn't… reduce gap").
   j. NUMBERS TRUE TODAY: claims_check above. Any FAIL is a must-fix; GATE lines go in the delivery message.
   k. SOUND: real sounds, not the same few repeated; on-screen sound that must be heard in sync is heard, never cut mid-word.
CALIBRATION: pace_check is a guide, not the verdict (the bar ad measures 33% calm). On the bar ad this critic said
"good not great" five rounds in a row while its director said "gas", "unbelievable", "so much better", "fire", "gorgeous".
The verdict tracks the 8a–8k items, the hook and the payoff, not polish in the abstract. Give "good not great" only
when one of those items is actually present, and name it.
Then: the verdict the owner would give ("fire" / "good not great" / "kinda ass"), and the 3–6 fixes
that would move it most, in order. Be specific and blunt; no praise padding. Don't edit any files.
EOF
cd "$AD"
claude -p "$PROMPT" ${CRITIC_MODEL:+--model "$CRITIC_MODEL"} --add-dir "$SK" --allowedTools Read Glob Grep --disallowedTools Write Edit Bash Agent \
  --no-session-persistence --output-format text > "$AD/renders/critic.md"
echo "critic → $AD/renders/critic.md"; head -c 1500 "$AD/renders/critic.md"
