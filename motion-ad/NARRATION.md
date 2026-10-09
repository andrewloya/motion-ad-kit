# Narrated ads: a voice over the whole video

These rules came from loya's notes (he founded LYRC) while building LYRC's narrated ads, one reaction at a time. His quotes are kept, labeled `(from the LYRC build: …)`. The owner's own notes get added the same way over time.

From the LYRC build: *"we should have some vids use narration for the whole thing to explain whats happening on screen and persuade users to use [the product] with a human tone. it shoudlnt be like sprinkled in at certain points. it should be heard over the whole vid for the most part for ones w narrations."*

A narrated ad is its own mode, not a music ad with a voice added.
- **Use it** when the owner asks, or when the subject needs explaining: a multi-step feature or service (an app flow with several steps, a booking → result process, a how-it-works).
- **Mix it up:** alternate narrated and music-driven ads. `ads-log.md` → Voice column.
- **What doesn't change:** every other rule. Real product, one camera, the brand palette, the hook rules, verified claims.

## What the voice changes
- **The voice is the timeline.** Write the script, generate the lines, then build every scene to the word timings. What the narrator says is on screen at the moment they say it: they say "hit generate" and the cursor taps Generate on "generate".
- **The narrator talks for most of the video.** Aim for voice over ~75–90% of the runtime. Silences are deliberate: a musical hit, the payoff landing, the CTA settling. They're never gaps where nothing is being said about what's on screen.
- **The track becomes the bed.**
  - Use the instrumental (most licensed tracks ship with an instrumental or stems; otherwise separate one with Demucs), ducked ~10–12 dB under the narrator (`mix.py` voice events do it) and back up in the pauses.
  - Sung vocals, if the track has any, stay out while the narrator talks, because two voices fight. One sung line can come up in a pause as a payoff.
  - Put the pauses between lines on the track's measured hits (`music_prep.py map`), so the edit still rides the music.
- **A narrated hook may run ~5.5 s**: two natural spoken lines take that long. It can when the premise is clear by ~2.5 s and its payoff lands on a measured hit; otherwise line 2 opens the body.
- **Anything on screen that has its own sound stays in sync with the bed.** When a shot shows content tied to the track (the track's words, a beat-synced animation), its track time must match the bed's at that moment. Easiest: ad time = track time, one continuous window.
- **The first spoken line is the hook,** and it's ALSO on screen as designed type (from the LYRC build: a narrated hook with no text reads as boring). The visual hook still gets full effort: frame 0 is the cover, the frame is full, every text element gets its own move (`HOOKS.md`). The stranger test applies to what the narrator says first.
- **No subtitles, but emphasis words, designed INTO the scene.** From the LYRC build, after v2 had captions on a strip (*"looks so shitty and just like stuck on there"*) and v4 had none at all: *"it should actually have some text to emphasize some things. but has to be worked into the scene not just thrown over the top willy nilly."*
  - Never subtitle what the narrator says, and never a strip, band or fixed caption spot.
  - Pick ~4–6 moments to emphasize: the stake, the number, the product's name for the action, the payoff. Each one's word(s) appear once, on the narrator's word, as part of the scene (STYLE.md → Text lives in the layout lists the ways).
  - Everything else the narrator says is SHOWN: they say "slide it to thirty", the real slider hits 30, big.
  - Sound-off viewers get the story from the picture plus those few designed words.
  - Ways to show what a caption used to say (all used in the LYRC build's v3 test):
    - the action lands on the narrator's word: the slider hits 30 on "thirty", Shuffle is tapped on "shuffle";
    - real labels do the naming: the product's own style names, date stamps, a DAY counter;
    - a detail repeated on every item says "same": identical tiles, the same row on every card;
    - the camera goes to what they name: zoom into the control, lean into the video.

## Pace: fewer beats, held longer
From the LYRC build, on v6: *"way too fast and too much going on."*
- A 30 s narrated ad gets **4–6 scenes**, one idea each. Pick the 3–4 steps that sell it and cut the rest (the fiddly sub-steps, like a drag, a shuffle or a tick per folder, can all go).
- Each key visual **holds 2–3 s** after it lands. The narrator keeps talking over the hold; the camera drifts slowly; nothing new enters.
- **The hook has ≤3 new elements** (v6 had 7 in 3.9 s). **Emphasis words ≤4** in the body (the hook's 2–3 printed words don't count).
- **Script ~55–65 words**, with real pauses.
- **Calm backgrounds.** Handheld footage or montage behind a scene fails calm time however slowly you cut it. Pick single-shot, slow clips for held scenes (run pace_check on the clip first).
- **The payoff wall stays lit.** A wall of 30 tiles playing is one idea, so give it `--allow` (≤3 s) instead of dimming it; v7 faded its wall to black to pass, and the payoff died.
- **Product UI must read on a phone.** A held UI beat that nobody can read is still "too much going on." Crop to the one part that matters (the one row and the control that changes it, not the whole editor) and scale it until its text is ~40 px+ at 1080 wide.
- **Calm is not still.** Fewer new things, never less motion: the held scene keeps animating (a long camera drift, layers parallaxing; never pulses on the beat). v7 held its scenes still and got *"not enough in animations"* (from the LYRC build) (`STYLE.md` → Craft; `craft_check.py`).
- Gate: `pace_check.py --narrated` (calm ≥30%, longest rush ≤3.5 s; it counts new content, so smooth motion passes). Recalibrated during the LYRC build: the ideal ad measured 33%; what the owner rejects is jumbled or dead, which the critic judges by eye.

## The script (human tone)
- **Length:** ~28–32 s of ad → **55–65 words** (see Pace). The default voice (Jessica, unless `brand.json` names another) reads ~2.2 words/s. `voice.py` prints each take's length: words ÷ seconds is the pace. Over budget? Cut words, not pauses.
- **Who the narrator is:** a friend who's in the customer's world, showing them a trick at 1 am. Their voice is the one named in `brand.json` (`BRAND.md` has how the brand talks).
  - Second person, contractions, short sentences, and one aside or laugh at most.
  - Specific: the real button name, the real count, the real time it took.
  - They are not the owner: never first-person about the owner's own work or life (from the LYRC build: never "my song").
- **Never an announcer.** No "introducing", "meet", "revolutionary", "game-changer", "unlock", "elevate", "seamless", "take your [thing] to the next level". Run the script through an anti-AI-writing pass (the spoken subset) if you have one; either way, read it out loud and cut every line you wouldn't say to a friend.
- **The shape** (a guide; the subject decides):
  1. **Hook** (≤2 s, one line): passes the stranger test.
  2. **The problem they know** (1–2 lines): the lazy version, said plainly.
  3. **The show** (3–5 lines): the narrator says each step as it happens on screen (from the LYRC build: "type what you want the clip to look like. hit generate. that's it.").
  4. **Proof** (1 line): the result in the world, or one verified number.
  5. **CTA** (1 line), spoken and shown: the CTA from `brand.json`, e.g. "comment LYRC and we'll DM you the link."
- **Whole spoken sentences, one take each, never chopped to match the on-screen chunks.** In the LYRC build, v29 voiced the hook as three fragments ("Your song is fire." / "Nobody knows." / "Yet.") placed on each word's reveal, and it was rejected. The line wanted instead: *"your song is fire, but nobody knows it...yet. let's fix that"*. Write the line as a person would say it (conjunctions, "it", the dramatic pause as "..."), generate it in one take, and let it run a little behind or ahead of the type. If it won't fit before a sung window, shorten a later line, never the hook's flow.
- **One connected story, not the headlines read aloud** (from the LYRC build: *"the script would need to be more descriptive and cohesive tho than just saying the words on screen"*). Each line hands off to the next (there: "Here's the fix. Drop your song into Lyric. It times every lyric to your voice…"). The on-screen headline and the narrator's line can name the same step, but in different words.
- **The narrator both explains and persuades.** Every "here's what's happening" line carries a "here's why it matters to you" beat. Don't spend two lines on either alone.
- **Numbers the narrator says** need the same verification as printed ones (`GOTCHAS.md`; list them in the ad's `claims.md` too).
- **Say the brand name the way the owner says it.** If TTS mangles it (spells an acronym out, or reads it as a different word), write it phonetically in the narration text (`BRAND.md` → How to say the name). From the LYRC build: the brand LYRC is said "lyric", like the word, never spelled L-Y-R-C (*"its pronounced 'lyric' not L-Y-R-C"*); TTS spelled it out or read it as "lurk", so the narration text says "Lyric". On screen it stays the logo.

## Making it
1. Write `pipeline/narration.json`: one entry per sentence or beat (`[{"id":"01","text":"…"}]`).
2. **ElevenLabs direct** (from the LYRC build: *"its WAY better cuz u can adjust creativity"*): `uv run --with requests python scripts/voice.py pipeline/narration.json assets/audio/vo --stability 0.0 --takes 3`.
   - It uses the same account and knobs as elevenlabs.io: stability 0.0 = **Creative**, 0.5 = Natural, 1.0 = Robust.
   - The key is `ELEVENLABS_API_KEY`, in the environment or in `~/.config/motion-ad/.env`. Never print it.
   - It writes 48 kHz wav plus word timings. mix.py needs the voice at the instrumental's rate (44.1 kHz for most tracks), so convert with ffmpeg.
   - Then check every take with Whisper (`music_prep.py words <take.wav> --from A --to B`). The heard text must match the script, and tags must not be read aloud.
3. Pick takes. The owner listens at delivery, so flag any line whose emphasis you couldn't judge.
4. TTS word end-times can run late (in the LYRC build they ran ~0.25 s past the real end of speech): place lines on the MEASURED speech end (Whisper or the waveform), not the last word's end-time. Place the lines as `"sfx": "voice"` events in `events.json`: a pause lands on each measured hit, and the narrator's first word lands just after frame 0.
5. Run `uv run --with numpy --with soundfile --with scipy python pipeline/mix.py … --duck 10 --words-out pipeline/words-ad.json`. That gives the premix, plus every word in AD time. `words-ad.json` from THIS mix is the timing truth (the critic reads it); older word files drift by a frame or two.
6. Build the scenes from `words-ad.json`: scene changes on sentence ends, the on-screen action on the word that names it.

Cost: about 400 characters of script × `--takes 3` ≈ 1,200 characters of the plan's monthly allowance per ad (the LYRC build ran on the Starter plan, 30k characters/month).

## QA (in addition to SKILL.md's)
- Whisper the FINAL mix in chunks, ~10 s each (`music_prep.py words assets/audio/final-mix.wav --from A --to B`): whole-file Whisper drops lines after a music gap. The transcript must match the script: words mushed under the music mean the bed is too loud.
- Voice over ~75–90% of the runtime, and no silence over ~0.8 s except the planned musical pauses.
- No subtitles, strips or bands. The ~4–6 emphasis words are designed into their scene, and the narrator's words land as actions within ±0.1 s.
- Every action the narrator names is on screen on that word.
- `fill_check.py` passes. A voice leading the edit is no excuse for small UI on black; the frame fills in every scene (STYLE.md → Fill every frame).
- Pace 2.4–3.0 w/s, and it doesn't sound rushed. If it's over, cut words, don't speed up.
