# "LYRC in Claude": a whole ad, music-locked (made for LYRC)

Verdict: **"i love it. this is fire"** after 20 versions. Learn the craft; never re-run its format, track, hook or layouts.
Files: `sheet.jpg` (whole-ad strip), `index.html.txt` (composition), `hook-plan.md` (the 6 hooks, ranked: the process done right).

## What makes it work
- **The product working, in the app people already use.** The other app's window is rebuilt from real frames; the
  product's widgets are rebuilt from their source. Nothing is shown that the product can't do: when the ad needed
  something the product couldn't do yet, the product got fixed and shipped BEFORE the ad.
- **Hook = pain, then the flip.** "STOP EDITING (manually)…" over a busy editor whose playhead keeps playing; the editor
  is crushed into one chat message, and the headline becomes "TEXT CLAUDE INSTEAD" in the same spot.
- **One continuous camera.** The message sends and becomes the chat; the camera dives into the result on the first
  sung word; the composer rises OVER the playing video with a focus pull; tiles fly out to a full-frame 2×2.
- **Music-locked, every cut on the beat.** The track's own dropouts and hits carry the beats. Cuts on a fitted grid
  (`scripts/beat_check.py`), because the stored BPM was wrong (120 stored, 132 real).
- **Readable.** Each line holds long enough to read; no half-empty frame.

## The notes that shaped it (each is now a rule in the kit)
1. A style with overlapping white words was swapped for a cleaner one; a batch must vary in style AND colour. Change only
   the segment the owner names.
2. Whisper misheard a word as a swear and the mute cut the audio: check "swears" by ear.
3. An aside must be readable, right after the line it belongs to; a moving playhead with the active word lit.
4. "way too much blank space": scattered debris doesn't fill a frame.
5. "the cuts… not on beat": measure the grid; never trust stored markers.
6. "too hard to read": more time came from starting the track EARLIER, never from repeating a bar ("do not duplicate it").
7. Rounded cards need the camera to rest where the corners show; close the gap under the hook type.
