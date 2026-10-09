---
name: motion-ad
description: Use when the owner wants a motion-design or motion-graphic video / Instagram reel ad for their business — a product or feature launch, an offer or drop, a case study, a "how it works", a viral moment, "one like the last one" — or wants hook variations of one to test as trial reels. Also on first use, to set up the business's brand (SETUP.md).
---

# Motion ad

## First: is the kit set up?
If `brand.json` still has `"_setup": true`, or `BRAND.md` still has blanks, run `SETUP.md` first (install check + a short
interview with the owner), then come back here. Never make an ad on the template brand.

## Overview
Motion-graphic reels (9:16, ~20–35 s) for the owner's Instagram: **the business's real product, carried by one
continuous camera, on a track the owner has the rights to, ending on the CTA from `brand.json`** (default:
`comment "WORD" for the link`). Two modes: **music-driven** (the track carries it) and **narrated** (a human voice
explains and persuades over the whole video, `NARRATION.md`). Mix them across ads. The hook gets the most effort: write
**6 hook ideas** (words + a visual concept each), pick the best, storyboard it, and build that one. Build extra variants
only when the owner asks for trial-reel tests (the `hook` variable keeps that cheap). First drafts must already be as
polished as the examples.

These rules came from ~30 rounds of notes by loya building LYRC's ads with Claude. Each one was earned by a reaction to
a real ad; quotes marked "from the LYRC build" show the taste bar. **The owner's own notes get added the same way**:
when they react to an ad, turn the note into a rule in the file it belongs to (STYLE, HOOKS, STRUCTURE, GOTCHAS…), with
their words as the why. Edit the rule; never just append a diary. That's how the kit learns this business.

**What carries over from ad to ad (the house):** the type (`brand.json` fonts, or the house kit: Space Grotesk + an
Instrument Serif italic accent, Archivo for the one huge hero word), motion-designer craft (`STYLE.md` → Craft: physics,
layers, texture, never vibe-coded), the brand palette (always, `STYLE.md` → Colour), eased continuous motion, real
output only (the real product, the owner's footage, real screens rebuilt 1:1, real numbers), verified claims, IG safe
zones, the CTA.
**What must be new every time** (from the LYRC build: *"the only things it should copy are the IDEAS from the example.
not the exact song, not the exact designs, not the exact positionings, not the exact hook"*): the track (or at least the
section of it), the footage, the story structure, the layouts and positions, the scene designs, and above all the hook,
visual and verbal. `ads-log.md` lists what every previous ad used; the new one must differ on every column.

**`examples/worse-song/` is THE bar for every motion ad** (*"thats fucking gorgeous… thats the ideal motion graphic
video we want to strive for"*): a story hook that acts out its line, a body that pays it off with the real product,
real numbers, clean craft. Its README lists the rounds of notes that got it there: watch it (https://github.com/andrewloya/motion-ad-kit/tree/main/example-videos) and read
that first. Also `examples/story-hooks/` (THE bar for hooks), `examples/claude-connector/` (a music-locked whole ad),
`examples/the-lift/` (camera and music-sync craft), and `examples/steal-this/` (the kit's own ad, made WITH this kit for a
non-LYRC subject, with its full paper trail: plan, claims, decisions, critic report, fix rounds). Most were made for LYRC: learn *how*, then build something for this
business that looks nothing like them. Claude can't watch an mp4: read the contact sheets and the compositions.

## Non-negotiables (each one earned by a reaction)
| Rule | Why |
|---|---|
| **A new ad is a new ad.** Different track (or section) from every row of `ads-log.md`, different footage, its own structure and layouts, its own hook devices; only the house style and principles carry over. The hero beats show THIS subject's own real product | three LYRC sessions re-shipped one ad's format (same track window, footage, positions, opener): *"cant be the same damn format w the same footage and shit every time"* |
| **The hook is the most engaging part of the video.** It acts out the story its line tells: characters, action, a twist, every spoken word riding along as kinetic type that does what it says, fast, edgy, readable (`examples/story-hooks/`). Words sell the feeling (HOOKS.md). Build the hook first, alone, and don't start the body until it's the best thing in the ad | *"hooks need to be the most engaging part of the video… otherwise they will scroll and the rest of the video doesn't matter"*; the story hooks were *"insanely better… fire"* next to three words on a 3D wall |
| **The premise is TRUE on screen, and every claim is shown.** Plan with a claim→proof table: each line the voice or text says has its proof on screen at that moment ("ready in 10 minutes" → a real clock running beside the real thing being made). If the point is variety, the outputs look varied at a glance | *"the point of the vid is that none of them look the same but they all look the same bc u used the same exact footage… u say 'cut to the beat' … but u show no graphics relating to that"* |
| **Show the real flow from the customer's input.** What the customer brings or does first (their order, their upload, their booking, walking in) → what the business does with it → the result they get. Compressed, never skipped (`STRUCTURE.md`) | *"we gotta include that shit like u upload ur song and it makes an adjustable template then u make projects from that"* |
| **Real product output only.** The actual product, store, food, app or service result; the owner's footage and photos; screens rebuilt 1:1 from screenshots (or from the source code, if the owner has it); real numbers; customers' words only with permission. Never fake UI, never AI-generated footage passed off as the business, never stock pretending to be them | "real output, never fakes" is what made the LYRC ads land; fake UI reads as an ad |
| One continuous camera; transitions are floods / irises / dives, never hard cuts | "continuous motion design, no hard cuts" |
| Every move eased (GSAP `expo/power/back/sine`); `steps()` only for counters | linear motion is the first thing that reads machine-made |
| **Nothing pulses to the beat.** No camera pushes, zoom bumps, shakes, scale pumps, breathing or glow pulses repeating on kicks, hats or hits; no outline flashing across cards. A big musical event gets ONE move at most (the hook's slam, a drop), and continuous motion is long eased drifts, not beat steps | word pumps "look weird/unnatural like a glitch"; a cut that surged the camera on 13 hits: *"we need to not do the pulsing to the beat"* |
| Info cards reveal one at a time, slow enough to read (~0.43 s apart) | "give the user a chance to read them" |
| Outgoing content keeps moving until a transition fully covers it | a frozen dim card under the iris dot was flagged |
| Music first: the track's drop lands on the product's magic moment; hits land on measured onsets, not a grid | the drop + the slam on the right word is what made the first LYRC ad |
| Every printed or spoken number/claim verified today, in the ad's `claims.md`; the product or offer must be live for customers | a feature shown in an ad was still admin-only; two posted counts were wrong |
| **Made by a motion designer, never vibe-coded.** No web cards, no boxes or chips around words, two type voices per frame at most, physics moves (anticipation, overshoot, squash, a whip that brakes), ≥3 moving layers, texture and light, and always animating: few new things, lots of motion on them (`STYLE.md` → Craft) | *"how vibe coded it looks. the hook especially looks super vibecoded. and not enough in animations"* |
| **Less, held longer.** One idea per scene, and each key visual holds 2–3 s after it lands. Cut beats rather than speeding them up: showing every claim means making fewer claims | *"way too fast and too much going on"*; each round of fixes added and nothing got cut |
| IG safe zone checked on every variant, every scene | caught by eye after delivery |
| **Spacing: no dead gaps.** Stacked things sit close as one composed block (30–80 px, never 200+); nothing parked at an edge while the middle sits empty (`scripts/gap_check.py`) | *"spacing is a vital thing… never leave too much gap between shit"* |

## Build order
0. **A reference video?** If the owner sent an ad they love, as a link or a file ("make this for my company"), follow `REFERENCE.md` first: break it down with `scripts/ref_breakdown.sh <link or file>`, write the breakdown and the transfer table, then continue here. Copy the IDEAS, never the footage, music, words or layouts.
1. **Gate.**
   - Is the subject live for customers right now (the product, the offer, the price, the location)? `BRAND.md` → claims.
   - If the ad shows an automatic part (a daily update, an auto-reply, a delivery promise), check it actually works today.
   - Verify every number you'll print or say and every URL/handle (one that belongs to someone else can't be printed).
     Write each into the ad's `claims.md` as you go.
   - Check the CTA automation (`GOTCHAS.md` → The CTA keyword).
   - Ask the owner only what you can't find yourself (which account posts it, the footage you need).
2. **Pick the track, then map it.**
   - A track the owner has the rights to use in ads (`BRAND.md` → Music), not used in any row of `ads-log.md`
     (including *(planned)* rows). If every track is used, a new section of one is OK; say which.
   - Add your *(planned)* row to `ads-log.md` now. Track + section, footage and stage (light or dark) are filled
     immediately, never TBD. Add the hook device as soon as step 3 picks it. Each cell must differ from every row above it.
   - Map it: `scripts/music_prep.py map / bars / grid / key` (`PIPELINE.md` §0).
   - Design the arc on its measured events (`STRUCTURE.md` → Map the track first), and write the claim→proof table
     (every line → its on-screen proof → its real source).
3. **Mode + hook.** Narrated or music-driven? A narrated ad writes its script now, and its first line is the hook
   (`NARRATION.md`). REQUIRED: `HOOKS.md` → "6 ideas, build the best one". Research, write 6 ideas (words + visual),
   rank them and pick one. Storyboard it every 0.25 s, then build and render the hook ALONE and check it before any body
   work. List all 6 ideas in the delivery message so the owner can ask for another.
4. **Scaffold + inputs.** `bash scripts/new_ad.sh <slug>` (a blank composition in the brand's palette and fonts), then
   `PIPELINE.md` §1.
5. **The hero output** (`PIPELINE.md` §2): the real product, the way customers get it — footage of the real thing, the
   real screen rebuilt with real data, a real before → after.
6. **Composition** scene by scene in the house kit (`STYLE.md`), in the brand palette, with this ad's own stage and
   layouts. The hook is one value of the `hook` variable (more values only if the owner wants variants).
7. **Audio**: the track (stems if needed) → mix → real SFX only where the cut is narrated or story-led → the voice if it
   has one (`scripts/voice.py`) → loudnorm −13 LUFS (`PIPELINE.md` §4).
8. **QA** (below), for every variant you built. Fix, re-render, re-check.
9. **Deliver**: the phone-size final (≤30 MB; plus any variants the owner asked for) to `finalsDir` from `brand.json`
   (and attached in chat if the app can), with the 6 hook ideas listed and the pick explained; complete the ad's
   `ads-log.md` row (drop *(planned)*) and add its hooks to `hooks-log.md`; say whether the CTA keyword is live. Never
   post anything: the owner posts (unless they've said trial reels can go out without their review: write that in
   `BRAND.md` if they do).

## The owner's eye: the gate before anything is sent
Checks passing isn't the bar. A LYRC test that passed palette, fill, transcript and IG zones was called "kinda ass".
Before sending:
1. Answer each question honestly, pointing at frames on the whole-ad sheet:
   - Is the premise true on screen?
   - Does every claim have its visual?
   - Is the real flow from the customer's input there?
   - Does any rebuilt UI look fake, or cover the product's output?
   - Is there any stretch over ~3 s with no new information or new real screen?
   - Does the hook pass the stranger test and look real?
   - Would a motion designer have made this frame, or does it look like an AI built a web page (`STYLE.md` → Craft
     tells)? Look at the hook at full size, not only on the sheet.
2. Write `<ad folder>/decisions.md` (the owner's rulings for this ad: what they banned or chose, e.g. "no invented
   dates or view counts", plus a "words never shown" list) so the critic doesn't ask for them. Then run
   `bash scripts/critic.sh <ad folder>`: a fresh Claude pass that looks at the sheets, the script, BRAND.md and the
   owner's past verdicts, and lists what they'd hate.
3. Fix everything it finds that you agree with. Tell the owner what you didn't fix and why.

Never describe an ad as a "step up" because the checks passed.

## QA checklist (every variant you built, not just the one you changed)
All scripts are in `scripts/`; `PIPELINE.md` §5 has the exact commands.
- Hook sheet at 0.25 s steps from 0 to the hook's end (`sheet.py`):
  - **Frame 0**: would it work as the reel's cover? Full and striking, not black or near-empty.
  - **Space**: is any third of the frame empty or flat for more than ~0.5 s? Is the focal element big (130–200 px
    type, footage/UI ≥80% wide)? Scattered debris over a dark stage does NOT fill a third, even though fill_check passes
    it (*"way too much blank space"*).
  - **Dead frames**: any flat flood colour held for more than ~0.15 s? Any text passing through text?
  - **Reading**: can you read each line fully before the next thing competes? Is the premise clear by ~2.5 s?
  - **Motion**: does something move in every frame, and does every text element enter with its own move?
  - **After the hook**: does the first scene land big?
- `beat_check.py` passes on every stretch of footage cuts: every cut on the track's beat grid (*"the cuts for the vids
  are not on beat. they need to be"*; stored markers were 40–200 ms off).
- `fill_check.py` passes: no ≥1 s stretch with ⅓ of the frame empty, anywhere (`--allow` only a deliberate "line"
  beat). Check the WHOLE-ad sheet as well as the hook: the body and end card fill the frame too.
- `pace_check.py [--narrated]` passes. Put an allowed payoff range in `pipeline/pace-allow` (e.g. `21.8-24.8`) so the
  critic uses it too. Busy source footage (handheld, fast-cut) fails pace on its own: screen clips with pace_check before
  picking them. It measures how often NEW content arrives, not motion: calm ≥30%, and for narrated no rush over 3.5 s.
  A rejected test was 22% (*"way too fast and too much going on"*); THE bar is 33%. What gets rejected is JUMBLED or
  DEAD, not motion: judged by eye.
- `pulse_check.py` passes: no repeating zoom bumps. Also search the composition for `yoyo`/`repeat:` on scale, glow or
  opacity: those are pulses too.
- The hook alone: `pace_check.py renders/hook.mp4 --hook` is advisory: the loved story hooks are 0–9 % calm. What
  matters is that every printed word reads and the story is clear by ~2.5 s.
- `craft_check.py <ad>` passes: ≥4 tweens/s, 0 linear eases, per-letter motion (*"not enough in animations"* was 2.4/s;
  liked ads 5.4–7.2).
- `qa_frames.py <render> --skip-until <hook end> --strips renders/qa` lists one-frame POPs, EDGE-CUT text and
  TOP-PARKED words, with a frame strip for each. Look at every strip; fix each one that isn't designed.
- `claims_check.py <ad>` passes: every number and offer word on screen or in the narration is in `claims.md`, checked today.
- `palette_check.py <render>` passes: the brand palette only; a flagged frame is OK only if it's footage or a product shot.
- Frame strip across the WHOLE ad per variant (`sheet.py`): the hook's background/props must be gone after the hook.
- IG overlay (`ig_overlay.py`) on the hook frame + every scene. Organic Reels zones: header y 70–170 (no text above
  ~230), like/comment rail x > 940 for y 1100–1720, caption/username y > 1580. Paid ads (Meta box): 270 top / 670
  bottom / 65 sides — say if a cut isn't ads-safe (`brand.json` → placement).
- Nothing appears then re-animates ("double pump"); nothing clips inside its mask; no frozen footage.
- `gap_check.py <render>` passes: no empty band over 170 px between stacked things, held 0.4 s+. Fix by moving the
  camera or scene to the type (or the type to the scene), never by shrinking the type.
- `media_check.py <ad>/index.html` passes: no `<video>` plays past the end of its file (a short clip holds its last
  frame: *"become static"*). Start the clip later or use a longer one.
- `npx hyperframes lint .` clean; audio: voice level, the drop, every hit.

## Red flags — stop and fix
- A track/section, footage, layout or scene order already in `ads-log.md`
- Walking an example's scene order, timings or end-card words instead of this track's own map
- Picking a track without adding a *(planned)* row first (a parallel session picks the same one)
- Scene timings from a BPM number or grid math instead of `music_prep.py map`
- "free", a price, a discount or "no card" that `BRAND.md`'s claims don't back today; a handle or URL that belongs to
  someone else; a real person's name in an AI-generation prompt
- "Make one in a different style" read as "throw out the structure": a new style changes the LOOK (palette use, type,
  transitions, camera language). The real product stays the hero from the drop on, one camera carries it, the hook has
  a stake. A kinetic-type showreel of words about the product "sucked" next to a real-product ad
- A reference chosen for craft alone: pick ones whose job matches ours (a product film that shows the product working),
  not motion-designer flex reels
- `diff` against the last ad shows only copy or number changes: that's a relabel, not a new ad
- A hook line that's already in `hooks-log.md` (reuse the ANGLE with new words and a new picture, never the line)
- Drawing a fake app screen or a fake product instead of rebuilding / filming the real one
- A hook that's a fact about the world, a made-up personal story, or reads like an ad
- Fewer than 6 hook ideas, or ideas that are the same angle reworded; building all 6 when the owner didn't ask for variants
- A hook whose visual is only lines rising over a background, where every word uses the same entrance, or which is too
  fast to read
- A hook that needs context about the business to make sense (a feature name, an internal count): it fails the stranger test
- Narration sprinkled at a few points instead of carrying the video, or a narrator who sounds like an announcer
- Vibe-coded frames: a web card floating on a blurred photo, highlighter boxes, outlined stamps, sticker chips, a mono
  kicker + numbered list, fade-up entrances, anything that arrives and then sits still
- Subtitles or text strips laid over the content; emphasis words belong designed INTO the scene (STYLE.md → Text lives
  in the layout). Zero text anywhere is also wrong: a hook with no type reads as boring
- A hook visual that's the literal illustration of its line: *"boring predictable visuals"*
- Showing a screen or product angle the owner dislikes as if it's the hero (`BRAND.md` → never show)
- Synthesizing a voice from noise (use real TTS), or a sound effect where the owner asked for a visual effect
- Any number, count or offer you didn't verify today
- Checking only the first seconds of a new variant

## Files
`SETUP.md` first run · `REFERENCE.md` "make this for my company" from a reference video · `BRAND.md` the business (who buys, voice, proof, claims, never-print) · `brand.json` palette,
fonts, CTA, voice, folders · `ads-log.md` what every ad used (differ from all of it) · `hooks-log.md` which hooks won ·
`STRUCTURE.md` map the track, story principles, ideas by subject · `NARRATION.md` the narrated mode · `STYLE.md` the
house kit · `HOOKS.md` hook rules + opening devices · `PIPELINE.md` commands · `GOTCHAS.md` bugs, claims, never-print,
the CTA keyword · `scripts/` new_ad.sh, starter.html, music_prep.py, mix.py, voice.py, sfx_pick.py, sfx_gen.py, the
checks (beat, pace, pulse, fill, gap, palette, craft, claims, media, qa_frames), sheet.py, ig_overlay.py, critic.sh ·
`examples/` the bar · `fonts/` the house kit (SIL Open Font License) · `vendor/` GSAP.
Related skills, if installed: `hyperframes` (the framework's own rules: install it, SETUP.md), `viral-hooks` and
`anti-ai-writing` (hook and copy craft).
