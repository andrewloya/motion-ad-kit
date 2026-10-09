# Structure — map the track, then build the story on it

These rules came from loya's notes (he founded LYRC) while building LYRC's ads, one reaction at a time. His quotes are kept, labeled `(from the LYRC build: …)`, because they show the taste and the stakes. The owner's own notes get added the same way over time. "The product" below means whatever this business sells: the app, the dish, the haircut, the garment, the coaching result. "The track" is music you own or have licensed for ads (your own, Epidemic/Artlist/Musicbed, a commissioned beat).

## What every ad needs (the principles)
1. **0 to ~3.5 s: the hook.** The whole ad lives or dies here. It's words × visual: an edgy, unexpected line about a stake the viewer owns, plus a visual hook with as much motion and craft, readable by ~2.5 s (`HOOKS.md`).
2. **The product does the job on screen.** Use real output, the thing the way customers actually get it, and land its magic moment on the track's biggest musical hit.
3. **Proof.** Show the result in the world (worn, eaten, booked, posted, on a lock screen, a customer reacting), something the viewer wants for their own life or business.
4. **One payoff number**, verified (against the ad's `claims.md`), or a real timestamp from the real run.
5. **The end:** the CTA from `brand.json`. On Instagram the default is `comment "WORD" for the link`.

Everything else is designed fresh for each ad: how many scenes, their order, whether there's a "rest of the business" beat, where things sit on screen. Two ads in a row with the same scene order is a red flag. So is a scene list that walks the order of one of the example ads in `examples/` (they were made for LYRC: learn HOW from them, never copy their subject, track, layouts or hook).

## Map the track first (the recipe)
The track's shape decides the story's shape. Do this before drawing any scene:
1. Pick the track: not one already used in `ads-log.md`, and not in a *(planned)* row. You choose a window A–B inside it; the ad can start and end anywhere in the track.
2. `music_prep.py map <instrumental or full track> --from A --to B` prints the measured events: BASS IN, bass out / BREAK, and the biggest hits. When the track has vocals, run `music_prep.py words` first so each event shows the word sung at it. The rest of the toolbox:
   - `bars`: per-bar low/mid/high energy, the track's shape (sparse intro vs full beat);
   - `key`: the track's key, for SFX notes in key;
   - `words`: free local Whisper on any section, words in track time;
   - `grid`: the measured beat grid that cuts and hits snap to.
3. Hang the story on those events:

| Measured event | Story job that fits it |
|---|---|
| The first BASS IN after a sparse intro, or a SILENCE → big hit when the track has no sparse intro | the hook exits (`HOOK_END`), and the product enters. Choose the window so this leaves the hook 2.5–4 s of reading time |
| The biggest BASS IN after a BREAK | the magic moment: the product's output lands |
| A short gap (~0.5 s) | a held breath: a tap, "the one", a single word |
| A BREAK (≥ 0.8 s) | a turn: the before→after, the line, the page going live when the bass slams back |
| Sung words that echo the story (only if the track has vocals) | put the matching scene on them (a lyric like "all in one place" = the pieces snapping together) |
| The last BASS IN | the CTA lands |

**Start the audio on a clean point** (from the LYRC build, on an ad whose audio opened badly: *"the audio sounds really weird on the start. should start audio at a better point"*). The window opened on the tail of a sung word over a 0.3 s instrumental stop, then the beat came back mid-bar. Before fixing it, look at the envelope of the first second (20 ms windows; vocal and instrumental separately if you have stems) and start where a sound begins: the beat coming back after a stop, a downbeat, or a vocal phrase's first syllable, with ~15 ms of pre-roll. Never start inside a word, inside a stop, or on a sung word the ad shouldn't carry (`BRAND.md` → never print). If the composition is already timed, keep it and trim the render instead (that ad dropped 19 frames from the render, and the mix's `--song-start` moved with it).

4. Choose the window so the magic moment falls around 4–7 s, which is where people who stayed past the hook decide whether to finish. Land scene changes on measured events (`map`, `grid`), not grid math from a BPM number. A BPM in a track's metadata or filename is often wrong (many say 120): measure it.

## Claim → proof (write it with the arc)
| Line (voice or text) | Proof on screen at that moment | Real source |
|---|---|---|
| "it takes ten minutes" | a visible clock or the real timestamps running while the work happens | the screen recording of the real run, not an estimate |
| "it does it for you" (from the LYRC build: "it cuts your clips on the beat") | the mechanism visibly doing the work (there: the track's waveform with cut markers snapping onto the beats, and the video cutting on them) | the product's own screen or process, rebuilt 1:1 |
| "none of them look the same" | 4–9 outputs side by side that look obviously different: different shoots, sources, styles, looks | several real sources, never one folder or one batch |
| "people keep coming back" | a real customer's words, order history or numbers on screen | the real message, review or record, shown only with permission |

A line with no proof gets a proof or gets cut.

## Show the real flow from the customer's input
Show it whenever the subject has a flow, which is almost always: whatever the customer brings or does first (their order, their booking, their upload, walking in the door) → what the business does with it → the result they get.
1. **The input**: the real moment where the customer starts (the real order form, the real booking page, the real upload screen, the real door and counter). In the LYRC build this was the real create screen where the artist uploads a song.
2. **What the business does with it**: the visible work, and when it's adjustable, show a hand adjusting it. In the LYRC build the lyrics transcribed and landed on their words, then cut markers dropped onto the beat and a hand dragged one to show it's adjustable.
3. **The result they get**, in the form they get it: the real output, at the scale the ad is about (one, or thirty). In the LYRC build that was videos made from the customer's own clips plus the stock library, in a chosen style.

Compress it, but don't skip it: in the LYRC build one song card (waveform + lyric chips + red cut markers dropping) did the whole input → work step in ~1.5 s.

## Ideas by subject (starting points, not templates)
| Subject | Input the viewer owns | Magic moment | Proof | Payoff |
|---|---|---|---|---|
| New product / feature launch | what it takes in, or what the customer brings | its real output, full-frame, on the hit | the output in use (worn, posted, shared, used) | its verified number |
| **App / software UI** | their name / data / account | the real screen, rebuilt with real data, doing its job; the UI itself is the hero, and samples of its output appear only where they earn it. For generated output: the prompt they'd type, then the one that looks fire after the tries | the result in the world (a customer using it, a filled calendar, a finished file landing) | a real count or time, tries / minutes from the real run |
| A service result (before/after) | their before state, the problem as they have it | the after, on the hit; the BREAK is the turn | the same subject shown before and after, real footage of a real job (with permission) | how long it took, how many sessions, from the real job |
| A physical product | the occasion or the need they'd use it for | the product in real use, full-frame, on the hit | it in the customer's world (worn, opened, on the table, a reaction) | a real number: units, days to arrive, review count |
| A local business / venue | walking in: the booking, the order, the door | the best real moment of the place (the pour, the reveal, the plated dish, the full room) | a real customer's reaction, a real review on screen (with permission) | a real count: years open, customers served, wait time |
| A case study of a real customer | their situation and their before state | their best result on the hit | real verified stats (with permission) | how many / how fast |
| An offer / drop / event | the date, the deadline, the scarcity the viewer cares about | the thing revealed on the hit | real sign-ups, a real queue, a real sold-out counter | the real deadline or quantity |
| A viral moment | the moment | the business's version of it | the comments | — |
| Something an earlier ad only named (yours, or one the viewer has seen) | the input | the part that was only NAMED: the real screen, the real steps, one control at a time, zoomed | the real result | its number, shown not said |

For the last row (from the LYRC build, where a launch ad had only named a feature that deserved its own ad):
- Show the real screen and steps, not the earlier ad's hero visual again (there: not a radial wall of 30 as the hero).
- A grid that mirrors the hook as the payoff is fine: in a test ad, an identical grid turning into 30 different tiles was its best idea.
- **Skip any screen the owner hates or has queued for a redesign.** In the LYRC build the app's "ignite" screen (BUILDING YOUR MONTH / ROLLING OUT) was hated, so the ad cut from the START tap straight into video #01 with a camera dive until the screen was redesigned. The move that worked: the camera dives into the START button while video #01 grows out of its centre, and the video fills the frame exactly on a measured hit, on the first frame of a new shot.
- **Only show what customers can actually get.** A step that looks open may be gated (a beta flag, a plan limit, out of stock, not yet launched). Check before showing it.

**Proof doesn't have to be a social post** (except when the hook is set on the feed, e.g. a reel-comment hook, where the feed is the natural payoff). The posted grid, the lock screen and the Story are what everybody reaches for first, and they've been done. Other places the result can land:
- a customer's screen recording or camera roll;
- a friend's text reaction;
- the confirmation email, the receipt, the order notification buzzing on a phone;
- the thing in the customer's hands, on their table, on their shelf, in use;
- the calendar filling up, the booking confirmed, the "sold out" badge;
- the file or result landing in Files, downloads or the inbox;
- a real review or message from a customer (with permission);
- the queue at the door, the full room, the window.

**No filler.** Every ~3 s adds new information or a new real screen. A stretch that re-states the hook (the same result shown again, a grey-out) is filler: cut it or make it show the next step of the flow.

**Real UI text is fine where ad copy would repeat.** If the real button says "ONE CLICK", show the button. Just don't write another ad's words as this ad's own copy.

**A window anywhere in the track is fine.** Get its sung words with `music_prep.py words` when you need them. If the ad shows content timed to the track (words, a beat-synced animation), make a LOCAL copy retimed to the window. Never edit the owner's originals.

**A hook line may carry into scene 1** as that scene's headline, if scene 1 owns the element from then on. Everything else the hook added hides under the transition.

**A promo for something with its own look** (the owner's own release, collection, launch, event): the thing itself is the subject, not the business.
- Palette: the brand palette like every ad (the thing's own artwork shows its own colours). Using the artwork's colours for the stage or floods needs the owner's OK.
- No "rest of the business" beat.
- Ending: that thing's own CTA ("out now" / pre-order / book / tickets), never "comment for the link" unless the owner asks.
- Check it is actually out or on sale (release date, stock, tickets) from the real source before the ad says so.

## A "rest of the business" beat is optional
Only the CTA is required. If a kit / "everything else you get" beat helps, give it a form native to this ad, like the LYRC artist-page ad turning it into the page's own link buttons. Never reuse another ad's upgrade-sheet grid.

## Technique, not order
Study how each change rides a musical event and how one camera carries the screen (`examples/`); never reuse another ad's order, timings, layouts or scene designs.

## The hook in the composition
Build the picked hook as one value of the `hook` composition variable (the `scripts/starter.html` scaffold), before the body. Extra values come only when the owner wants variants. Every variant shares the body exactly, owns its DOM, tweens and SFX block (`HOOKV`), and hides everything it added under the transition at `HOOK_END`. See `HOOKS.md` → "6 ideas, build the best one".
