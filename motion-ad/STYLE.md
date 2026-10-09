# Style — the house kit (what stays the same) and the choices each ad makes

The kit below is shared by every ad, and that includes the colours: **the brand palette from `brand.json`, always: black, white and the 1–2 brand colours.** The CHOICES (which stage, layout, props, end-card wording) are made per ad, written in its `ads-log.md` row, and must differ from the last ad's.

These rules came from the notes of loya, the founder of LYRC, over about 30 rounds of building LYRC's ads. His verbatim reactions are kept as `(from the LYRC build: …)` so you can see the taste and the stakes behind each rule. The owner's own notes get added the same way over time. "The owner" is the business owner using this kit: the person who gives the final yes and whose taste the skill learns.

## Type (all files in `fonts/`) — house kit, every ad
This is the default kit. When `brand.json` → `fonts` names the brand's own fonts, they replace the house font **by role** (headline, accent, mono, hero, titles); every role below keeps its job and its rules whatever font fills it.

| Role | Font | Use |
|---|---|---|
| Headlines, body, UI | **Space Grotesk** (`SG`, 600 for heads, tight `-0.045em`) | hook lines 112–168 px, labels |
| The accent word | **Instrument Serif Italic** (`IS`), in the ad's accent colour | ONE word or phrase per line (*booked*, *friday.*, *the one.*) |
| Tech texture | **JetBrains Mono** (`JB`) | small labels, counters, timestamps, stats line |
| Big titles (optional) | **Bebas Neue** | big sheet/section titles |
| The hero word | **Archivo variable** (`Archivo-VF.ttf`, axes `wdth` 62–125, `wght` 100–900) | the ONE star word of a scene, huge (300–600 px, fills the width), wide and black, with its letters punching in width/weight as they land. (From the LYRC build, a layout the founder liked: *a star word huge in wide black Archivo, the line small and condensed*) |
| Real UI | the product's own fonts | only inside rebuilt product UI |

**Two type voices per frame, at most** (a hero word + one supporting voice). A frame with a mono kicker + a Bebas title + a sans line + a serif-italic accent is a web page, not a shot (from the LYRC build: that was exactly what one early hook looked like, and it got sent back).

## Colour — the brand palette (fixed)
(From the LYRC build, after test hooks came out red and green on a blue brand: *"why are they red? should be using proper colors, blue and black and white."*)

The palette comes from `brand.json` → `palette`:
- white `#fff`;
- black `#000`;
- `stage` — the background the ad sits on (white, or black/near-black like the ink and night tones the palette names);
- `ink` — the opposite of the stage, for type;
- `accent` — accent words;
- `flood` — scene-change floods and big colour fills;
- `glow` — glows, selection, gradients;
- `extra` — any further colours `brand.json` explicitly allows, and no others.

That's all. No new hue per ad: no red, green, purple or cover-colour floods, accents or stages unless they are in the palette.

Colour from elsewhere appears only where it's real content:
- inside rebuilt UI, the product's own states (its dark or light panels and borders, a status red, an error ✗, a success ✓);
- inside footage, product photos, covers and the product's own renders.

Variety between ads comes from:
- the stage (white vs black);
- which brand colour leads (flood vs glow);
- layout, footage, hooks and motion.

It never comes from a new hue. Set the tokens in `scripts/starter.html`: `--stage` is `#fff` or `#000`/the palette's dark stage, `--ink` is its opposite, and `--accent`/`--flood` (and the glow) are the brand colours from `brand.json`. Avoid full-screen linear gradients on dark (H.264 banding).

## Craft: made by a motion designer, never vibe-coded
(From the LYRC build, on an early ad: *"how vibe coded it looks. the hook especially looks super vibecoded. and not enough in animations."* The same was said about early motion tests: *"plain/look like they were vibecoded"*.) The fixes that won the founder over there are the rules here: **physics reads premium, fake effects read cheap**, and **one idea per scene, many layers**.

**The vibe-coded tells (what an AI builds by default in HTML). Never:**
- **A web card as the scene:** a white or dark rounded rectangle with a drop shadow, floating centred over a blurred photo (the LYRC build's "THE PLAY" sheet).
- **Fake chrome on type:** highlighter rectangles behind words, outlined "stamp" boxes, pill chips, sticker rectangles, tag boxes, black bars as redaction, see-through backings. (From the LYRC build, on a slot-reel window: *"making it feel cheap."*)
- **A web page's type stack:** a mono small-caps kicker ("THE PLAY · 5 STEPS"), 01/02/03 numbering, a headline, a serif-italic accent word, all in one frame.
- **Web motion:** fade-up (`y 30 + opacity`), everything on the same ease and duration, elements that arrive and then sit still, constant-speed drift.
- **Flat and unlit:** sharp vector shapes lit by nothing, no texture, no depth, nothing in front of or behind anything.

**What reads as motion design instead:**
1. **Type IS the graphic.** One hero word per scene, huge (Archivo, width-filling), everything else small. Its letters move as letters: per-letter width/weight punch on landing, staggered drops that squash, masks that slice it, scale jumps between shots.
2. **Physics, not effects.** Things have mass: anticipation before a move, overshoot and settle, squash on impact, a camera that whips and brakes (from the LYRC build: a flat camera push got *"looks like shit"*; a real whip with braking and motion blur at peak speed was loved). Nothing just fades in.
3. **Layers in depth, all moving.** Every shot has ≥3 depth layers (the world: footage or a stage; the type; a foreground element or texture). They parallax at different rates as the camera moves. One-idea scenes read flat (early LYRC motion tests); layering fixed them.
4. **Texture and light.** Subtle animated grain over everything; halftone or print texture on props (a brand mascot, if there is one); light that moves (a slow sweep across the hero word on its landing, never on every kick); shadows that come from the scene's light. Nothing is clean, flat vector.
5. **The real world and the graphics touch.** The product's own output makes a strong world for a hook (from the LYRC build: a wall of real renders tells a stranger "videos" at frame 0; for any business, a wall of real finished work, real plates, real products, real results), as long as it sits back behind the hero word. The founder's references from the LYRC build: Rheon Maro, cut out on white with a VFX gag every ~1.5 s, and catireel_'s "1234!", a new scene on every beat. Use the owner's footage with the subject cut out (a subject mask) so the type passes behind the subject; graphics collide with, get grabbed by or react to the footage.
6. **Always animating, rarely new.** Holds keep moving, but with moves that don't read as new stuff. `pace_check` predicts each frame from the last by motion, so these are calm: a slow camera push or drift, parallax between layers, a word or card sliding, rotating or scaling. These count as NEW content, so save them for landings: light sweeps, flashes, fades, letter weight/shape changes, text changing, many videos playing at once. One playing video at a time; a wall of renders behind the words plays at half speed, blurred or dimmed, and comes fully alive only on its reveal (from the LYRC build: both hook tests put a wall of 12–16 finished videos behind the words, and their own moving content fought the hook). "Calm" means no new idea, never a frozen frame; don't freeze the wall to pass the gate. In the hook, each of its ≤3 elements DOES something about once a second (gets grabbed, cracks, flips, gets pulled out of frame), so the few things on screen stay alive.

**Holding still without freezing** (measured by `pace_check`):
| Calm (use in holds) | New content (save for landings) |
|---|---|
| a slow camera push / drift, parallax between layers | light sweeps, flashes, fades |
| a word, card or video sliding, rotating, scaling | letter weight/width breathing, shape changes |
| one video playing | several videos playing, text changing, a blinking cursor |
- **Enforced:** `scripts/craft_check.py <ad>` (animation ≥4 tweens/s, 0 linear eases, per-letter motion) and `pace_check.py`, which counts new content, not motion. The look itself is judged by eye and the critic (question 6e).

## Props (optional — use when the story wants them)
- **A brand mascot** (optional; only if the brand has one and `BRAND.md` says so). When used: face or pose swaps with an elastic squash, bob `sine.inOut`, it lives in a corner and never covers a headline, the CTA or product UI. It is a prop, not the opener — at most 1 of an ad's 6 hook ideas opens on it, and rest it entirely for ads after one that used it.
- **The cursor/tap** (from a LYRC ad): a real pointer that taps real buttons, with a ring on press.
- **Phone / lock screen / IG chrome**: rebuilt at 1:1 from screenshots, checked against the IG overlay.

## Motion vocabulary (GSAP; every move eased)
| Move | Recipe |
|---|---|
| Line rise | text inside `overflow:hidden` mask, `yPercent 115→0`, `expo.out` 0.55 |
| Accent write-on | `clipPath inset(… 100% …)→0`, `power3.out` + an SVG underline drawing `power2.inOut` |
| Whip in | `x:-560, blur 16px → 0`, `expo.out` 0.5 |
| Pop | `scale 0→1, rotation -25→0`, `back.out(3)` |
| Drop + bounce | per-letter `y:-820→0`, `bounce.out` 0.62, stagger 0.035 (mask overflow visible) |
| Flip | `rotationX -100→0`, origin top, `back.out(1.5)`, parent `perspective:900px` |
| Number slam (once!) | hidden until its moment, then `opacity 0→1, scale 1.3→1, y -18→0`, `expo.out` |
| Camera move | `moveScreen()` between rects, `expo.inOut` / `expo.in` into a landing; motion blur 3–7 px at peak speed |
| Scene change | a flood circle from the focal point (`power3.in` 0.42), an iris (`power2.in`), a dive, a scan wipe — outgoing content keeps moving until covered |
| Letter punch (hero word) | per letter: `font-variation-settings` `wdth 62→125→100`, `wght 300→900`, with `scaleY 1.25→0.92→1` squash; stagger 0.03–0.05, `expo.out` then `back.out(2)` settle |
| Mass land | anticipation (`y +12` over 0.08 s, `power2.in`) → throw (`expo.out`) → overshoot → squash on contact (`scaleY .88, scaleX 1.08`) → settle (`elastic.out(1,.5)`) |
| Whip + brake | camera `x` across 1.5 screens: `expo.in` 0.18 s, then `expo.out` 0.35 s from the other side; directional blur (SVG `feGaussianBlur stdDeviation="30 0"`) only at peak speed |
| Parallax rig | 3 layers in a `perspective:1400px` parent at `z` −600 / 0 / +300; move the rig, never one layer alone |
| Light sweep | a soft white band (`mix-blend-mode:overlay`) crossing the hero word, `power2.inOut` 0.6 s, on a hit |
| Cards in (real UI only) | one at a time ~0.43 s apart, each thrown in with Mass land, image Ken Burns `1.14→1` over 3 s. Never the plain fade-up |
| Holds | one long camera drift or push across the whole hold (`sine.inOut`, 2–4 s, 3–8%), layers drift at different rates — nothing ever freezes, and nothing pulses to the beat (no surges, no breathing, no `yoyo`) |
Never: linear eases, anything pulsing to the beat (camera surges, zoom bumps, word pumps, breathing, glow pulses; from the LYRC build: *"we need to not do the pulsing to the beat"*), flashing outlines, hard cuts, elements that appear and then re-animate. A new ad may add moves (a new transition, a camera language) — write them into this table when the owner likes them.

## Fill every frame (the whole ad, not just the hook)
The look this kit is built on is a full frame. (From the LYRC build: a narrated test was full in the hook, then went back to small tiles on black, a half-width player and an end card in the top third, and got sent back.)
- **Focal element big in every scene.** Footage, a product shot or a player at ≥80% of the width, or type at ≥110 px. A row of 3 tiles fills the width (~330 px each) or becomes one big tile.
- **Small real UI gets the camera, not a shrink.** Real product panels are often small (LYRC's were ~440 px wide). Don't show the whole panel small. Crop to the control being used and zoom until its text is ≥40 px and the control spans the width. Move the camera from control to control as it's used (dropdown → slider → button).
- **Nothing sits on flat black or white.** Behind UI and type: footage, the product's own output (blur ~8–10 px and dimmed, not a 30 px smear that reads as empty), or the product's own texture.
- **The end card fills too.**
  - Logo ≥300 px wide.
  - The CTA (`comment "WORD"` by default) ≥110 px.
  - A full-width comment bar.
  - Over the ad's last footage or its best product shot, not black.
- **Palette-only still needs variety.** The palette locks hue, so a month of videos must differ in everything else:
  - footage brightness and place (day vs night, indoor vs outdoor, nature vs city, the owner's own footage vs cleared stock);
  - type scale and placement (giant single words vs blocks of type);
  - layout.
  Include at least one bright beat; an all-dark body reads as one video (from the LYRC build: a critic's note on an all-dark cut).
- **Deliberate exception:** one short typographic "line" beat (≤3 s, big centred type ≥130 px), like the LYRC psst ad's "you make the music."
- **Enforced:** `scripts/fill_check.py <render> [--allow <line beat range>]` flags any ≥1 s stretch where ⅓ of the frame is dead.

## Text lives in the layout (every ad)
Text never sits on a translucent band or strip laid over the content. (From the LYRC build: that looks *"stuck on there if its not properly integrated into the layout."*)
- A headline gets its own space in the composition: the product moves or scales aside for it, or it's part of the scene (a sign, a UI label, a comment, a card).
- Emphasis text (from the LYRC build: *"some text to emphasize some things… worked into the scene"*) is a few words at key moments, built INTO the scene. Ways that work:
  - **Object:** the word IS a physical thing with mass: letters that drop and squash, get grabbed, slide under a product element, get torn; or a label that's really in the footage or the real UI. Never a box drawn around a word (sticker chip, outlined stamp, highlighter rectangle): that's fake chrome (Craft).
  - **Depth:** the word lives in the scene's space: on a tilted plane with the phone, between the footage and the UI, parallaxing with the camera, or behind the subject (cutout).
  - **Full-frame beat:** the word gets the whole frame for a moment, and the camera flies through or into it to the next scene.
  - **Interaction:** the word reacts to the product: a UI element slices it, the cursor drags it, a product shot shoves it aside, it flips into the next word.
- Never: a translucent band, a subtitle row, a fixed caption spot, or text that ignores what's behind it.
- **Never park the words at the top of the frame** over a scene that carries on below them. The words go where the action is (the centre mass), and nothing leaves a dead band. (From the LYRC build, on "20 A DAY" sitting over the top of a static wall: *"the words at the top are never a good idea we dont wanna leave weird empty space."*)
- **A spoken claim gets acted out, not just a number stuck on a still.** (From the LYRC build, on "They posted it. Twenty times a day." over a still wall plus "20 A DAY": *"should be better. so bare rn."*) Show the posting happen: posts firing out and landing, a counter climbing to 20 inside the action, the day filling up. Whatever the claim is, show it happening.
- The body mostly shows. Emphasis is ~4–6 moments per ad, and the hook always carries designed type.

## Composition habits
- Hook text starts at y ≈ 250 (below IG's header), left ~80, max width ~920.
- Every hook has a living background that illustrates its line — never text on a plain field.
- Product UI is the real screen re-built at 1:1 from screenshots or source, then scaled.
- When the product's real output swaps to another version of itself (a different look, colourway or variant), switch with a crossfade (old fades, new settles from 1.07×), never a punch zoom.

## End card — parts are fixed, words are chosen per ad
Parts, in order (and filling the frame; see Fill every frame): the brand logo (≥300 px; skip it when the CTA's WORD is the brand name, or the name prints twice) → one line for THIS ad (its own words — not the last ad's line, and not an example's: the LYRC psst ad's "lyric videos *in seconds.*" is for LYRC only) → the CTA from `brand.json`, by default `comment "WORD" for the link` (WORD in the accent colour) → an IG comment bar that types WORD and taps Post → the site or handle → one stats line.
Stats line = only claims verified today for the thing shown (`BRAND.md` → claims table, and `GOTCHAS.md` → Counting claims). **Never print "free", a price or an offer** ("free trial", "no card", "% off", "from $X") unless `BRAND.md`'s claims table says it's true today, for the exact thing the ad shows. Before delivery, check the keyword automation behind the CTA is live (comment WORD, see the reply or DM arrive); if you can't check it, say so in one line. An ad that promotes the track itself ends differently (see `STRUCTURE.md`).

## Spacing: no dead gaps
Stacked elements read as one composed block: a headline and the thing it's about sit about 30–80 px apart at 1080 wide, never 200+ (from the LYRC build: *"never leave too much gap between shit"*). Check every frame, not just the cover. `scripts/gap_check.py` enforces it.

## Sound
The track at −13 LUFS, and REAL sound effects: few of them, each one made for its moment.
- **Music-driven ads get no sound effects.** The track is the sound. (From the LYRC build, on the jelly ad: the founder heard ~70 synthetic blips, then 12 real pack sounds leveled under the mix, and said *"remove all SFX. sounds cheap asf and just wrong"*. SFX worked on the narrated story hooks (trial 4b, "lowkey fucking gas"), where the sounds act out a cartoon.) So: narrated or story-led cut → a few real SFX that act the story; a music-driven cut carried by the track → `events.json` is `[]`.
- **Fewer.** One sound per big story moment (a crowd rushing in, a spray can, a snatch, a slam, a reveal), about 8–12 in a 30 s ad, never one per move. (From the LYRC build: 68 synthetic whooshes/pops/thumps in 32 s got *"wtf u doin w those sound effects lmao ur just spamming the same exact few"*.)
- **Real, not synthetic. Pack first.** `python3 scripts/sfx_pick.py find cartoon impact` searches the SFX library (a pro pack of real recordings: cartoon impacts/bloopers, colossal impacts, UI, whooshes, bass drops, crowds/walla, foley; `SETUP.md` says where to get one) plus every generated sound. `sfx_pick.py cut <file> <name> --from S --dur D` trims it to `sfx-library/cuts/<name>.wav` at 48 kHz and prints its peak: place the mix.py `"sample"` event at **t = hit − peak** so the impact lands on the frame. Nothing fits → generate one with `scripts/sfx_gen.py "<exactly what you hear>" <name>` (ElevenLabs via fal, cents). The procedural whoosh/thump/pop/ticks are placeholders for drafts only.
- **Pick sounds that act the story** (from the LYRC build's trial-4b hook): a boing when cartoon eyes pop up, a creaky crash when the band lands on the crate, a rocket on BLOW UP, a falling bass on the jaw drop, dealt cards as videos fly into the wall.
- **Never the same sound twice in a row**, and let the track's own hits be the hits.
- **Level each one against the track.** mix.py scales every `"sample"` to full volume first, so `gain` is the sound's peak (0–1), not a multiplier. Aim for 6–10 dB under the music bed (RMS over 300 ms at the hit); the first pass of the LYRC build's sound swap landed 15–24 dB under, which is silent. A click can sit lower than a whoosh because its energy is all in the transient.
- **When on-screen content has its own sound that must be heard in sync** (a video whose words are readable and synced to its audio, a person talking to camera, a demo whose sound is the point), **that sound is heard** (and on music-driven cuts, only then: the beat carries the rest, PIPELINE.md §4): it plays under the ad (`--vocal-windows` covering every span where that content is on screen; the narrator ducks it, never cuts it). A window that ends while the content is still on screen reads as broken sync (from the LYRC build: *"the audio is off on it now for when the lyric videos go"*).
- Voice: the Eleven v4 narrator via `scripts/voice.py` (NARRATION.md); a friend, not an announcer.
