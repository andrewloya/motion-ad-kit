# Gotchas — every bug the ads hit, and the fix

These rules came from loya's notes while building LYRC's ads (LYRC is a lyric-video app for musicians; loya is its founder). Quotes marked "from the LYRC build" are his reactions to real ads. Your own notes get added the same way: when something breaks twice, add a row with the symptom, the cause and the fix.

"The track" is the music the ad is cut to. "The owner" is the person who gives the final yes.

## Visual / animation
| Symptom | Cause | Fix |
|---|---|---|
| Every cue lands late by the same amount (words, slams, exits all ~0.3 s after their sound) | a tween placed at a NEGATIVE time (`ft(-0.3, …)` to have letters already landing on frame 0): GSAP shifts the whole timeline later to make room, so every later position is off by that much (the kit's own demo ad, before it shipped) | never position anything before 0; for a frame 0 that's already in motion, start the tween at 0 from a mid-way state instead. Grep the composition for `ft(-` and `, -0.` positions |
| A hook's background (ghost words, footage) shows behind later scenes | the per-variant layer faded in, never out | every hook variant hides everything it added by ~3.4 s (`tl.set(el,{opacity:0},3.4)` under the flood); check a mid-ad frame of EVERY variant |
| Number "double pumps" (shows, then re-slams) | it rose with its line, then got its own scale tween | `gsap.set(el,{opacity:0})`, then one entrance tween at its moment |
| Big glyph/letters clipped | text sits in an `overflow:hidden` line mask | `tl.set(mask,{overflow:'visible'}, t)` just before the move (or mask overflow visible for kinetic words) |
| Pulses on the beat (words, camera, glows) | beat-synced `scale 1.04→1` on words (from the LYRC build: "like a glitch"); camera `surge()` on every hit plus pushes on the hats, `yoyo` glows ("we need to not do the pulsing to the beat") | remove; holds get one long eased drift; a big event gets one move. `pulse_check.py` catches camera bumps |
| Outline highlight walking across cards looks glitchy | glow borders flashing in sequence | cut it; reveal the cards one at a time instead |
| Card sits frozen & dim while the iris dot grows | the exit tween ended before the transition covered it | exit runs until the cover completes (0.6 s `power2.in` falling/fading) |
| Render comes out frozen (nothing animates) | GSAP loaded from the CDN; a network drop during the render's compile step skips it (the log says `Failed to download CDN script`) | bundle it: load a local copy of `gsap.min.js` from the ad folder, never the CDN |
| A hook test shows the old version | `hooktest.html` is a copy of index.html made before the edit | re-make the copy before every test render, delete it after (lint fails while it exists) |
| Element pops in at full state before its tween | `fromTo` with `immediateRender:false` and no initial `gsap.set` | always `gsap.set` the pre-state for anything that enters late |
| Two tweens fight over `y` | a float overlapping a camera move (`moveScreen`) | schedule floods/floats after camera moves end |
| Switching the same footage between looks feels jumpy | a per-switch zoom ("punch") on the screen | crossfade, no punch |
| Blank screen for ~0.15 s between two looks (or scenes) | the outgoing one's exit leaves the frame empty | start the next one earlier (a 16th note) so its entrance fills the gap |
| The product's output is shown at a weak moment (a nearly empty frame, one lonely element) | wrong moment chosen | audition several moments on a contact sheet (`sheet.py`); pick one where the output is full and building |
| The hero shot shows a variant customers don't actually get (an old or default look; from the LYRC build: "just not a preset we use"); a batch whose tiles all share one look | picked from the whole library; one colour across the batch | the HERO shot ("your video") shows the product the way customers actually get it, not a variant nobody uses (the same non-default look shown deliberately as a restyle was fine). Change only the part the owner flagged: when they name one segment, leave the others as they were. Showing range (a batch, a wall of outputs): every tile a visibly different look AND a visibly different colour; check the contact sheet, not the ids |
| Cuts off the beat (from the LYRC build: "the cuts for the vids are not on beat. they need to be") | a stored BPM or someone's markers (a template's, an editor's, a track's metadata) are NOT a beat grid: a stored 120 BPM for a 132 BPM track put its markers 40–200 ms off; hero cuts hand-placed "near" markers inherit the error; a 1-frame dissolve lands the visible cut a frame late | `scripts/beat_check.py --grid-out grid.json` gives the track's constant-tempo grid. Hero cuts on bar starts, montage cuts every 2 beats, cuts as hard cuts (a ~0.0001 s dissolve, never a 1-frame one), cut times ~10 ms before the beat, then beat_check the final render. Half-speed copies: re-measure, the slow-down moves the cuts |
| Black bars inside source clips (2.39:1 cinema-format footage, screen recordings with bars) | the 16:9 file keeps the letterbox bars baked in | crop each source to its real picture size (e.g. `crop=iw:iw/2.4`) before comping; check the real picture height of every source you use |
| Footage freezes mid-shot | the segment is longer than the clip | next.t − t + 0.3 ≤ clip length − in-point; add a segment. When filling slots from a pool, filter the pool to clips ≥ the longest slot |
| A swear (or any word on the never-print list) shows on screen or is heard | the on-screen text came from the source as-is; a censor alone isn't enough | switch the word off in your working copy of the text AND mute the audio span (`mix.py --mute`) |
| Tile font renders as system Impact | `@font-face` named like a system font | rename (`ImpactTile`) and use that name in the markup |
| A slam/shake on the drop is invisible | the effect moves only the footage, and a layer with a dark/solid background sits over it | pick a layer arrangement that leaves the footage visible, or skip the effect and let the visible layer's own hit carry the drop |
| Video card vanishes on the white page | its content is mostly white, on a white stage | give the screen a dark bezel + drop shadow while it's a card (`boxShadow` spread in pre-scale px) |
| Cursor blinks out between repeated taps | each tap's move tween starts from opacity 0 | follow-up taps start from the cursor's current spot at opacity 1 (`tap(..., visible = true)`) |

## Audio
| Symptom | Cause | Fix |
|---|---|---|
| A whisper or breathy effect "sounds awful" (from the LYRC build: "psst sounds awful") | speech synthesized from filtered noise | never synthesize speech from filtered noise; use a real TTS whisper (see PIPELINE.md → narration) |
| Trimmed clip is silent | `-ss` placed after `-i` with `afade`: fades use the original timestamps | seek on the input (`-ss A -t D -i in.wav`) |
| Hit lands early | the beat-grid formula drifts ~40 ms | measure the stem onset |
| On-screen content looks out of sync (its own sound, a voice or a sung line, plays only in a short window and cuts out while the visual is still on screen) | the clip's own sound is only mixed in for a short window | when on-screen content has its own sound that must be heard in sync, play it: cover every span where it's on screen with `mix.py --vocal-windows`; the narrator ducks the track, never mutes the clip's own sound |
| The track or clip sound cuts out oddly at the end (from the LYRC build: "the audio cuts out weirdly at the end w the vocals") | the window stopped mid-line with an 80 ms fade | end each window on a phrase end (check the stem's RMS), or `mix.py --vocal-fade 0.6`; never chop a word |
| A graphic sits in front of the words (a file icon over its own filename) | icon and label laid out in the same spot | icons and props never overlap text: stack them (icon above, words below) and check the frame |
| The product screen looks made up | cards and an invented waveform/chart with markers instead of the real screen | rebuild the REAL screen from the screenshot or source, and read what it shows (timings, values, items) from the real data. Never type data by hand. The owner's point: what's on screen must actually be how the product's real data is |
| Proof shots contradict the line before them | the script names how it works ("cuts clips from a link"), then the proof shows something made another way | the proof matches what was just said: after a line that names an input or source, every proof shot is made from that input (3 different examples, not one) |
| A UI screen flashes for a frame before its transition (an empty upload box before its scene) | the next scene's element was visible before the cover move finished | set the incoming scene's pre-state up front; step through every frame of each hand-off ±0.5 s |
| A typo in the real data shows on screen (from the LYRC build: "say 'worry' instead of 'worrY'") | the real text was printed as-is | real data, but fix obvious typos and casing on screen |
| Product UI crops look sloppy (text cut at the frame edge, a dead band above, the subject low and to one side) | the real window was scaled and placed, not framed | treat every crop as a camera framing: the subject fills the width with margin and is centred, nothing gets cut by the frame edge, and there are no empty bands. Check a 0.15 s strip of the section. The owner asked for the framing to be fixed on every one of these crops |
| A process animation looks jumpy (items appear in a few batches) | the items are revealed in groups, not as the process reaches them | the playhead/progress runs and each item lands as it's reached; items start appearing during the line that describes them, not at the end |
| The viewer still doesn't know what the product does | steps ("upload, then slide to 30") with no result named | say AND show the result, in the customer's terms (from the LYRC build: one song turns into many completely different videos, new footage and new style each time), and name where it comes from |
| SFX spam (the same few synthetic sounds 60+ times) | `mix.py`'s procedural sfx used for every move | ~8–12 real sounds (`sfx_gen.py`, `"sample"` events), one per big moment |
| A sound-pack sound lands late, or `mix.py` can't open it (`Bad 'PEAK' chunk`, 96/192 kHz) | pack files have pre-roll before the hit; some WAV headers break libsndfile; `mix.py` resamples by plain interpolation | always `sfx_pick.py cut` first (48 kHz, readable) and place at t = hit − the printed peak |
| `ffmpeg … aresample=resampler=soxr` fails ("Requested resampling engine is unavailable") | this ffmpeg build has no soxr | `aresample=48000:filter_size=64` (what `sfx_pick.py` uses) |
| Each hook variant needs its own SFX | one sound plan per variant | one `events-<v>.json` per variant → `mix.py` → `final-mix-<v>.wav`, mux after render |
| A re-edited track (jumping to a later section) sounds broken at the splice | many beats run in 2-bar A/B pairs; jumping onto a B bar breaks the pattern | splice only onto the same bar of the pair (correlate the bars to find them) |
| An isolated vocal or stem from elsewhere (an a cappella, a stem pack) doesn't line up | it's a different version of the track (its length differs from the master) | split the master you're actually using with Demucs instead |

## Tooling
| Symptom | Cause | Fix |
|---|---|---|
| A headless `claude -p` build stops halfway with an empty report | it was started as a harness background task, which dies when the launching session ends (it died twice) | launch long builds detached (`nohup zsh run-x.sh > log 2>&1 &`); resume from disk with a resume brief |
| Lint: multiple root compositions | more than one `.html` with `data-composition-id` in the folder | only one per folder; keep backups as `versions/*.html.txt` |
| Lint: duplicate media discovery | the same `<img src>` twice | use a `background-image` div for the second |
| Demucs: `No module named numpy` | the isolated environment has no numpy | `uvx --with numpy --with soundfile --from demucs demucs …`; cut the track window with ffmpeg first (a 12 s window splits in ~10 s) |
| `timeout: command not found` | macOS has no `timeout` | use `curl --max-time`, or run long jobs in the background |
| zsh reads `"$F[a]"` inside an ffmpeg filter string as an array lookup | zsh treats `[a]` as a subscript | write `${F}[a]` |
| Shortening a narrated ad without leaving the beat | — | splice the TRACK by whole bars at a measured hit, the same bar of the A/B pair (spectral match), then re-place the voice lines |
| zsh passes `$LIST` as one argument | zsh doesn't word-split variables | use `$(seq 0 0.25 4)`, explicit lists or `xargs` |
| zsh doesn't split `PY="uv run --with numpy python"` into words | same | `${=PY}` |
| A banned word or scene (a never-show item from BRAND.md or the ad's notes) reaches the screen through a wall tile | offset tiles reach the line before it, and a wall slowed behind the end card runs past the planned window | cap every tile's source time before the banned moment's line starts, and check each tile's last frame |
| Media built in JS never shows up | hyperframes finds `<video>/<audio>/<img>` in the static HTML | write them in markup and animate them from the timeline |
| Text shows at full state on frame 0 | the pre-state was never set | set every late element's pre-state up front (`gsap.set` opacity / clipPath / yPercent) |
| Premix clips before loudnorm | soundfile writes 16-bit by default | write `subtype='FLOAT'` (`mix.py` does) |
| A flat colour frame (~0.4 s) at every flood | the flood element sits above the incoming scene (global z-index) | place it in scene order, directly under the scene it reveals |
| Empty frames as an iris opens | the iris opens before the new scene has content | start the scene's entrance BEFORE the iris (content already there as it opens) |
| Lint: duplicate media on intentionally identical reposts | the same file twice | offset one copy's `data-media-start` by a frame |
| `drawtext` filter missing in ffmpeg | this build has none | label frames with Pillow (`sheet.py`) |
| Fetching a whole footage library for one ad is slow and heavy (110 clips ≈ 380 MB) | the pool is the whole library | pre-pick a pool of ~30–40 clips from one or two shoots and pull only those |
| Zooming a long stack of items cuts off its last item | the zoom scales from the stack's default centre | scale from the visible point (`transformOrigin` at the item you're showing, or `panelTo`) |
| Captions hidden under the stage video | captions sit earlier in the page than the camera's content | captions must come LATER in the page (or a higher z) than everything the camera carries |
| A CSS rule like `#x span{opacity:0}` hides the wrapper span too (a counter rendered empty) | the selector hits every span | target a class (`.ch`), not every span |
| Typewriter caret can't follow the text | hidden characters still take up space | put each character in a span with `font-size:0` and `tl.set` it to the real size at its time (`typeOn` in starter.html); the inline caret after the spans follows by itself |
| `fill_check` passes a half-frame of dim, blurred background | it only catches flat areas | look at the sheet too. A mostly-blur scene is still thin: bring the content forward |
| Stale numbers from notes, memory or an old ad (from the LYRC build: a note said 112, the real all-time count was 798) | a remembered number | the day's check in the ad's `claims.md` beats any memory (see Counting claims) |
| Lint: repeat can be −1 | `Math.floor(DUR) - 1` goes negative on a short comp | `repeat: Math.max(0, Math.floor(DUR) - 1)` |
| SendUserFile rejects the delivery | 30 MB cap | phone copies at crf 21 (~19 MB for 30 s 60 fps) |
| A config or data file contains a signed URL with an access key id | the tool exported it with the link in it | scrub signed links and keys before copying the file anywhere shared |
| Scratch frames gone next session | scratch intermediates are temporary | the pipeline regenerates them (frames render in minutes) |

## Safe zones & claims
- IG header covers y 70–170 → no HUD/timecode there; headlines start ~230+.
- Like/comment rail x > 940, y 1100–1720 → keep pickers, CTA bars, badges left of ~930.
- Caption/username y > 1580 → nothing important below ~1560.
- Paid ads need Meta's box (270 top / 670 bottom): an ad built to the organic safe zones above is organic-safe only (LYRC's first ad was).
- Every number in an ad is a claim. Count what the CUSTOMER sees, verify every number today, and write each one in the ad's `claims.md` (claim | source | checked date). `scripts/claims_check.py` fails on any number on screen or in the narration that isn't in it. BRAND.md lists where to verify each recurring claim.
- **LYRC's posted ads said "14 models" and "36 folders". Both were wrong** (13 and 35): the counts included things users can't see.

## Counting claims (what customers actually see)
- Count what a customer can see and use. Leave out retired, archived, empty, hidden, admin, internal and test rows, and the owner's own account and use. (LYRC build: a folder count dropped from 35 to 34 within one afternoon when a folder was emptied, so the printed figure was "30+ folders".)
- Say which thing you counted. "Claimed" is not "published" is not "active" (LYRC build: 45,384 page names claimed, 267 published). Print the one that's true for the claim.
- A number that depends on a plan, tier, size or option is true for that one only. Print the one that makes it true, or don't print the number. (LYRC build: "20 a day" was true for the top plan only.)
- Take limits from the real source (the setting, the config, the cap on the slider the customer actually uses) and the business's own published wording, not from a guess or a memory.
- If the count query times out, use an all-time count or a narrower window, and write which window in `claims.md`.
- Anything else: find the table or page the thing is written to, and count only what customers see.
- Round down to a "+" figure that survives a month of growth ("2,400+" for 2,441); never round up.

## Offer gates (what "free" and other offers can honestly mean)
Never print "free", a price, a discount, "no card", a guarantee or availability unless BRAND.md's claims table says it's true today. A feature or product must be live for customers to be in an ad. Re-read the pricing and plan source each time; plans change.

| What you want to print | When it's honest |
|---|---|
| "Free" next to anything | only what is free today. A thing listed as open to free accounts but unusable on free (LYRC build: some AI models were listed for free accounts, but free had 0 credits) is not free: never print "free" with it |
| "Free to start" on an end card | true for signing up. Pair it only with features that work on the free tier. Never print "free" next to the paid step (an export, an AI generation, posting) |
| A price, a discount, "no card", a guarantee, a delivery time, availability | only if BRAND.md's claims table says so today. LYRC's "no card" was never verified: don't reuse a claim like it |
| A feature or number that belongs to one tier | print the tier that makes it true (see Counting claims) |
| A feature in beta, preview-only or behind a flag | not a customer step in an ad unless confirmed live for customers. If real customers (not the owner) are already using it, treat it as open |
| A new product or feature | must be live for customers. LYRC's ads couldn't mention anything not launched yet (e.g. a multi-account feature that was preview-only, the Mac app, 4K export) |

## Never print
- **A real person's name or likeness in a generation prompt**, even when the line or lyric names them ("Jaxson Dart", "kobe bryant"). The models' real-person rule rejects it or makes a lookalike. Rewrite it as a description.
- **Example URLs or handles that belong to someone else.** Taken in the LYRC build: `lyrc.studio/you` (a real user's page), `drake`, `byeloya` (not the owner's page). Check before printing any example slug, handle or URL: look it up and see if it's taken. Safer: show the brand's own domain with a typing caret, or the owner's own page.
- **Another person's content**: covers, pages, renders, photos, reviews or clips that aren't the owner's own assets. Customer words or content only with permission.
- **Overclaiming words ("every", "all", "always") for something the product does selectively.** LYRC places its cut markers on SOME beats (the cut density decides), not every one. Say "perfect cuts on the beat", never "cuts on every beat", and don't draw a marker on every spike either. (From the LYRC build: "say 'every beat' which isnt true, its more selective than that.")
- **"it" where the brand does the work.** Name it: the narration says the brand (spelled phonetically if the TTS mangles it, BRAND.md → How to say the name) and the screen shows the real spelling. (From the LYRC build: "rn u say 'it' instead of 'LYRC'.")
- **A word the product doesn't do.** If the page links out to YouTube, don't say it plays videos. LYRC's artist page links to YouTube/TikTok, so the line was "your YouTube", not "videos".
- **A feature whose automatic part is broken.** In the LYRC build the artist page's weekly "newest release" refresh reported success, but only 3 of 69 pages refreshed in 14 days. Don't claim "updates itself" until it's fixed.
- **Screens the owner dislikes.** Skip them and cut straight from the start to the result (LYRC's batch-building animation, "BUILDING YOUR MONTH / ROLLING OUT", was skipped). Write the owner's dislikes into BRAND.md → never-print.
- **A mock UI that looks fake or covers the output.** Rebuild Instagram and the like 1:1 from a real screenshot. Real IG shrinks the video into the top area when the comment sheet opens: the sheet never sits on top of the output. (From the LYRC build: "looks like a fake IG comments section, also overlaps the lyrics on screen, bad UX.")
- **One footage source for "variety".** 30 videos from one shoot all look alike. Mix the owner's shoots with other real sources (licensed real stock, real screen captures) and say "stock" when you use stock.
- **An effect or overlay that paints its own white or coloured background over the footage.** A full-frame wash hides the footage it's meant to show. Render it with the footage showing, or don't use it. (From the LYRC build: "the white/colored background of all those movements takes away from the footage." On looks the owner called boring: "those look boring.") Anything the owner bans goes in BRAND.md → never-print. No 3D card flip between proof videos either.
- **Test uploads as footage.** Clips named "QA …" or odd-ratio test files in the owner's library aren't their shoots.
- **AI-generated b-roll passed off as the business.** Banned in ads. (From the LYRC build: "we dont want this to seem like cheap AI.") Libraries mix real and AI footage, so check each clip's source before using it, and treat an unverified source as not usable. Real footage = the owner's own shoots, real stock whose source you've verified, and captures of the real product. Before reusing an old render, check which clips it used.

## The comment keyword (CTA automation) — check before delivery
If the ad's CTA is `comment "WORD" for the link`, the automation behind the keyword has to be live before posting. There's usually no API key for the automation tool (ManyChat, or whatever `brand.json` names), so check it in the owner's logged-in browser, read-only. Never create or edit an automation.
- **Tool:** claude-in-chrome, or any browser tool that uses the owner's logged-in session.
- **What to look for:** a live automation with a Comments trigger on the keyword.
- **Several workspaces:** a tool like ManyChat can have one workspace per connected Instagram account. Check the right one, and look at its Settings → Instagram before trusting a list. The workspace switcher may show only one account, so go straight to the workspace URLs the owner gave you. An old workspace with an expired plan and no Instagram connected is dead: its run history is history, not live.
- If you can't check, or the keyword has no automation, the delivery message says so in one line: "comment WORD needs an automation before posting".

## Marketing art
Owner-approved assets only (BRAND.md → approved assets folder). If it's empty, use the owner's own covers, photos, logos and pages, real product assets and real renders. Never unknown-source AI frames: they could be someone else's content.
