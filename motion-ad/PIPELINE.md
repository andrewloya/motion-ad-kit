# Pipeline — how the ads are actually built

`SK` = this skill's folder (`~/.claude/skills/motion-ad`). `AD` = the ad folder `new_ad.sh` made. `SP` = a scratch folder
for heavy intermediates (stems, frames); use the session scratchpad or `/tmp`, and delete it when the ad ships.
Every python script runs with `uv run --with <deps> python $SK/scripts/<script>.py` (the deps are in each script's
docstring; `-h` prints it). The format: 1080×1920, 60 fps, H.264, −13 LUFS.

## 0. Scaffold, then map the track
```bash
bash ~/.claude/skills/motion-ad/scripts/new_ad.sh <slug>
```
Gives a BLANK composition (`scripts/starter.html` in the brand's palette and fonts: camera/flood/rise/typeOn/panelTo/flip
helpers and a 6-hook scaffold), a local GSAP, empty `claims.md` and `decisions.md`, and the folders below. Never start
from an example's composition: read them for technique only.

**The track** (`BRAND.md` → Music says where the owner's tracks live and what they're cleared for):
- A track the owner owns or has licensed for ads (their own music, a commissioned beat, Epidemic / Artlist / Musicbed
  with an ads licence). A trending sound from IG's library can't be baked into a motion ad: the edit is locked to the
  track, so the track must be in the file.
- No track at all is fine for a narrated cut (`mix.py --inst none`), but a quiet bed under the voice usually plays better.

`scripts/music_prep.py` (deps: `--with numpy --with scipy`; `grid` also `--with librosa`):
- `map <track> [--from A --to B] [--ad-start S] [--hits N] [--words W.json]`: the measured BASS IN / bass out / BREAK /
  SILENCE / hit events, with an ad-time column. `STRUCTURE.md` → Map the track first says how to hang the story on them.
- `bars <track> [--from --to] [--bpm N]`: per-bar low/mid/high energy: the shape where `map` is noisy (sparse intros).
- `grid <track> [--from --to] [--ad-start S] [--out grid.json]`: the fitted beat grid and every bar start. Footage cuts
  go ON this grid, ~10 ms before the beat. A BPM in a filename or tag is often wrong: measure it.
- `key <track>`: the key, plus the notes to use for `mix.py` pops in key.
- `words <audio> --from A --to B --out W.json`: free local Whisper (large-v3-turbo) with word times; swears flagged.
  Use it on the track's vocals (which word lands on which event), on every narration take, and on the final mix.
- `cut <track> --from A --to B --out SP/window.wav`: the ad's window at 48 kHz, for stems and the mix.

## 1. Inputs
| Need | Where it comes from |
|---|---|
| Track choice | A track (or section) no row of `ads-log.md` used, including *(planned)* rows. Write the row first. |
| Stems (only if a vocal must drop out under narration, or one sung line must come up in a pause) | `uvx --with numpy --with soundfile --from demucs demucs --two-stems=vocals -o SP/stems SP/window.wav` (free, local, ~10 s for a 12 s window). A stem the producer gave you counts only if it's the SAME version (same length, lines up). |
| Footage | The owner's real footage (`brand.json` → footageDir, or ask). 9:16 where possible, with motion and faces/hands/product in it; a shoot no ads-log row used (reserve it in your planned row). Never test clips, never AI b-roll passed off as the business, never stock pretending to be them. Check each clip covers its segment (a clip that runs out freezes). Rotated phone footage: check `ffprobe` rotation and bake it. |
| Product UI (apps, sites, dashboards, booking/checkout flows) | Rebuild it 1:1 in the composition from real screenshots (or from the real source code if the owner has it), filled with real data: the owner's own account, never a real customer's. A screen recording works for a fast beat, but rebuilt UI is sharper and lets the camera move through it. |
| Physical product, food, venue, service results | The owner's photos and footage of the real thing. Product cut-outs: `npx hyperframes remove-background` or any background remover, on the owner's real photo. |
| Logos, brand art | `brand.json` → logo; `BRAND.md` → approved assets. Owner-approved only; never unknown-source AI art. |
| Numbers you print or say | Verify each today and write it in `AD/claims.md` (claim · source · date). `GOTCHAS.md` → Counting claims. |
| Customer words, reviews, results | Only real ones, with the customer's permission, and the owner's OK to show them. Never invented. |

## 2. The hero: the real product
Pick by subject (`STRUCTURE.md` → Ideas by subject):
- **A UI subject** (an app, a booking flow, a site): the rebuilt screen with real data IS the hero. Crop the camera to
  the one control in use (text ≥40 px on screen), move from control to control as it's used, and show the real result.
- **A physical product / food / venue**: the owner's best footage of it, full-frame on the hit; the graphics live
  around it (cut-outs so type passes behind it, labels that ride with it), never a shrunken photo in a card.
- **A service result** (a cut, a clean, a design, a coaching result): the real before → the real after, with the real
  time it took. Same angle, same light: an honest before/after.
- **A case study**: the customer's real result, with permission, and the real number.
Prepare footage to the shot: trim with ffmpeg (input-seek: `ffmpeg -ss A -t D -i in.mp4 …`), slow a background clip to
½ (or ⅓–¼ with `minterpolate=mi_mode=mci` at tile size) behind a fast hook, denoise night footage (`hqdn3d`), and make
every clip last its whole time on screen (`media_check.py` catches the ones that don't).

## 3. Composition (`index.html`)
- Root `data-composition-id` 1080×1920, `data-fps="60"`, one paused GSAP timeline in `window.__timelines`. Helper
  `ft(t, el, from, to)` = fromTo with `immediateRender:false` (seek-safe). Every tween eased; `steps()` only for counters.
- **One continuous camera.** `#screenWrap` (the hero) travels between named 9:16 rects `R` via `moveScreen(t, from, to,
  dur, ease)`; surrounding UI groups move with `map(a, b)` so they stay locked to it. Floods / irises / dives are the
  only scene changes.
- **Media must be static HTML** (`<video>/<audio>/<img>` written in the markup with an id); the framework discovers media
  from the markup, not from JS. A `<video>` without an id renders frozen.
- **Hook variants** are a composition variable: `<html data-composition-variables='[{"id":"hook",…}]'>`, read once with
  `window.__hyperframes.getVariables()`. Each variant owns its DOM (hidden unless active), its tweens and its exit, and
  hides everything it added under the transition at `HOOK_END` (check a mid-ad frame of EVERY variant).
- Lint: `npx hyperframes lint .` (only one root html in the folder: keep backups as `versions/*.html.txt`).
- Preview: `npx hyperframes preview` (opens the studio in a browser).
- Render: `npx hyperframes render . -o renders/ad-v1.mp4 --fps 60 --quality high [--variables '{"hook":"h2"}']`
  (~45–90 s for 30 s). Render the hook alone first: set the composition's `data-duration` to the hook's end, or render
  and trim.
- The `hyperframes` skill (SETUP.md) has the framework's own rules: read it for anything this file doesn't cover.

## 4. Audio
0. **Keep the audio rebuildable from the ad folder.** Copy the window (and stems) to `assets/audio/` and write the exact
   commands into `pipeline/mix.sh`. Scratch folders get wiped; a revision shouldn't rebuild the bed from nothing.
1. **The window:** `music_prep.py cut <track> --from A --to B --out assets/audio/window.wav`. Start on a clean point
   (`STRUCTURE.md`): a downbeat, the beat returning after a stop, or a phrase's first syllable, with ~15 ms pre-roll.
2. **Narration** (narrated mode, `NARRATION.md`): `pipeline/narration.json` = one whole spoken sentence per entry, then
   `uv run --with requests python $SK/scripts/voice.py pipeline/narration.json assets/audio/vo --stability 0.0 --takes 3`.
   Whisper every take (`music_prep.py words`), pick, and place them as `"voice"` events.
3. **Sound effects** only on narrated or story-led cuts, and only real ones: `sfx_pick.py find <words>` in the library,
   `sfx_pick.py cut <file> <name> --from S --dur D` (prints the peak: place the event at t = hit − peak), or
   `sfx_gen.py "<exactly what you hear>" <name>` (fal.ai, cents). A music-driven cut on the track gets none.
4. **The premix:** `uv run --with numpy --with soundfile python $SK/scripts/mix.py --inst assets/audio/window.wav
   --stem-start A --song-start A --dur D --events pipeline/events.json --duck 10 --words-out pipeline/words-ad.json
   --out assets/audio/premix.wav` (`--vocals` + `--vocal-windows` when a sung line must come up; `--no-fade` keeps a
   frame-0 hit sharp). Written as FLOAT.
5. **Loudness:** `ffmpeg -i assets/audio/premix.wav -af loudnorm=I=-13:TP=-1.0:LRA=9 -ar 48000 assets/audio/final-mix.wav`.
   The composition's `<audio>` points at `assets/audio/final-mix.wav`; lint and preview fail without it.
6. **Variants with their own sound:** one `events-<v>.json` → `final-mix-<v>.wav` each, then mux after the render:
   `ffmpeg -i renders/ad-<v>.mp4 -i assets/audio/final-mix-<v>.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21
   -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart renders/<Business> <name> ad N - <v>.mp4`.

**A scene needs more time in a music-locked ad**: start the track EARLIER by whole bars and shift every later timeline
position by the same amount (one offset added inside `ft` / `tl.set` and the media `data-start`s). NEVER repeat or loop a
stretch of the track to buy time (*"just start the song's audio earlier do not duplicate it"*). Whole bars keep every
later cut on the beat: re-run `beat_check.py`, and re-sync the hook to the music that now sits under it.

## 5. QA commands (all variants)
```bash
S=~/.claude/skills/motion-ad/scripts; V=renders/ad-v1.mp4
uv run --with pillow python $S/sheet.py $V renders/sheet.jpg 0 8 240 $(seq 0 0.5 30)          # whole ad, every 0.5 s
uv run --with pillow python $S/sheet.py $V renders/hook-sheet.jpg 0 8 240 $(seq 0 0.25 4)    # the hook, every 0.25 s
uv run --with pillow python $S/ig_overlay.py renders/ig-2.5.jpg --video $V --at 2.5           # IG UI over a frame
uv run --with numpy --with opencv-python-headless python $S/pace_check.py $V [--narrated]
uv run --with numpy --with opencv-python-headless python $S/pulse_check.py $V
uv run --with numpy --with pillow python $S/fill_check.py $V [--allow a-b]
uv run --with numpy --with pillow python $S/palette_check.py $V [--allow a-b]
uv run --with numpy --with opencv-python-headless python $S/gap_check.py $V
uv run --with numpy --with opencv-python-headless --with ocrmac python $S/qa_frames.py $V --skip-until <hook end> --strips renders/qa
uv run --with librosa --with numpy python $S/beat_check.py $V --audio <track> --song-start <A> [--from --to]
python3 $S/craft_check.py .
python3 $S/claims_check.py .
python3 $S/media_check.py index.html
bash $S/critic.sh .                                   # runs most of the above, then a fresh-eyes Claude critic
```
zsh won't split a `$LIST` into arguments: use `$(seq …)`. A frame that looks blank or frozen on a sheet may be
mid-transition: re-sample that second at 0.1 s steps before calling it a bug.

## 6. Deliver
- The final, phone-size (≤30 MB): `ffmpeg -i renders/ad.mp4 -c:v libx264 -preset slow -crf 21 -maxrate 7M -bufsize 14M
  -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "<finalsDir>/<Business> <ad name> ad N - <hook>.mp4"`.
  Never overwrite an earlier final: a new version gets a new number.
- The message: what it is in one line, the 6 hook ideas with the pick and why, anything you didn't fix and why,
  whether the CTA keyword is live, any claim that changes soon.
- Update `ads-log.md` (the row, no longer *(planned)*) and `hooks-log.md`. When the owner reacts, turn each note into a
  rule (SKILL.md → Overview) and record the verdict in the row's Status.
- Clean up every round: keep the current version's renders and named finals; move older renders to the Trash; delete
  scratch frames and stems the moment they're encoded (a frame dump can fill a disk: pipe frames straight into ffmpeg).
