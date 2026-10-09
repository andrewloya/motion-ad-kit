# loya's rulings for this ad (the critic must respect these)
- HOOK LINE IS GIVEN (loya picked it 10-05, keep it exact, Jessica says it): "If you've watched a worse song than yours blow up, here's what they did that you didn't." It replaces "if you were smart…" (that hook, "the lift", stays the craft bar: _skilltests/H and the skill's example/hook-the-lift).
  Why it works (loya): identity friction ("wait i am smart"), a tutorial framed as sauce worth stealing, not "my boring tutorial to buy my product".
- Colours: blue, black, white only. Other hues only inside footage / covers / lyric renders.
- No subtitle strips or bands. ~4–6 emphasis words designed INTO the scene. The hook always carries designed type.
- No invented dates, view counts or stats in any UI.
- A 30-video wall / grid as the payoff is allowed (it's the month).
- Skip the app's Rollout ignite screen ("BUILDING YOUR MONTH / ROLLING OUT").
- The "bad"/lazy video is never a LYRC render. No pixel-decay "buffering" look (v5's hook visual read as buffering).
- Shuffle swaps clips (that's what the product does); it doesn't change the style.
- Show the real flow: upload song → template (lyrics timed, cuts on the beat; the drag-a-cut beat may be cut for pace, since the pace ruling outranks it) → Rollout (his shoots + LYRC stock, one folder per video) → visibly different videos → a month.
- Narrated the whole way (Jessica), human tone, ≤32 s.
- PACE (loya on v6, 09-30): "better but i think its just way too fast and too much going on lowkey." v6 measured calm time 18% (his liked cover-art ad: 70%). Fewer scenes (4–6), one idea each, key visuals hold 2–3 s, hook ≤3 new elements, ≤4 emphasis words. Cut beats rather than speed them up. Must pass pace_check.py --narrated.
- v8 (loya 09-30, on v7): the template beat must read on a phone (crop to the lyric line + cut markers, text ~40 px+,
  filling the frame, calm background). The WALL STAYS LIT under "a month of posts from one song": it gets
  pace_check --allow (≤3 s, one payoff picture) instead of being dimmed; the "one song" card may land over the lit wall.
  The three proof videos must read as different at a glance (type colour, size, layout), ≥2.2 s each; the 30-slider hold
  was trimmed to pay for it. No white smear out of the hook. The end card fills the frame (bigger sheet over the wall).
  Measured pace_check runs WITHOUT the wall's --allow, so a lower number there is expected; the gate is the --allow run.
- LOOK (loya 09-30 on v7): "how vibe coded it looks. the hook especially looks super vibecoded. and not enough in animations." Then on the hook-only test "the lift" (_skilltests/H): "oh bro A is fukcing SICK". v9 uses that hook as-is and brings the body to the same craft; the redacted-card look (hook and end card) is retired.
- Words never shown: "Hoe" (a goodbye lyric) — no render, tile or wall may display it; check any widened time window.
- The payoff range for pace_check's --allow lives in pipeline/pace-allow (update it if the wall moves).
- v9 (loya 09-30): the hook IS "the lift" from _skilltests/H, ported as-is (same still wall of 16, same stolen video, same
  SMART → STEAL → ROLLOUT, same sound). Its wall is a STILL on purpose (H measured 3% calm with a playing wall, 49% frozen);
  don't ask for it to play. Body = the same film: the camera dives into the empty slot (upload → template → Rollout live
  there), the proof videos come out of the wall, the payoff is the wall lit, the end pays off the hook (the stolen video is
  thrown back into its slot; comment "LYRC" in the hook's type + IG's real comment bar). The redacted "THE PLAY" card is gone
  for good. The hook wall is H's seed-7 Rollout run; the body wall is this ad's seed-91 run (both real renders of goodbye).
- Real UI inside the slot (dropzone, cut bar, Configure panel) and IG's comment bar are rebuilt product UI, not web cards.
- Emphasis words: the hook's SMART / STEAL / ROLLOUT, then 30, ONE SONG, LYRC (all Archivo, the hook's one font).
- 10-05 rulings (loya):
  - Hooks sell the FEELING (being heard, praise, respect), not the means ("more videos").
  - The template line names LYRC and doesn't overclaim: "Lyric times your lyrics and adds perfect cuts on the beat" (TTS text "Lyric"; never "it", never "every beat"). On screen: no "on every beat", and markers on some beats, not every spike.
  - LYRC is said "lyric", never spelled: the last line is "comment lyric for the link." (the screen still shows LYRC).
  - No pulsing to the beat (pulse_check). v10 (no pulses) was "95% good": keep its body.
- Trial 4 (10-05, loya's brief): the hook (0–5.86) is a NEW story hook in the style he called "insanely better… fire"
  (skill example/hook-story-styles/C, "the words act it out"); same line, same take, same bed. Body + end card = v11.
  The hook is meant to be fast (pace_check --hook is advisory; the loved story hooks measure 0–9 % calm), so the whole-ad
  narrated rush flag inside 0–5.1 s is expected; the body alone passes pace. Plan: pipeline/hook-plan-t4.md.

## AUTOPILOT trial 1 "worse song" (10-06, loya's notes on t4b) — these rulings supersede the Rollout ones above where they clash
- KEEP the story hook 0–5.858 exactly (line, take wh-t3, visuals, sounds). Only change: the hook wall's top-right tile was a Tiled Wave
  render (white wash); it is now a real Airplay render tile (LYRC stock rooftop). The hook wall is a still on purpose.
- The body promotes AUTOPILOT, not Rollout. It pays off the hook: what they did = posted the song constantly; how = one template + Autopilot.
  Order: 20 A DAY over their wall → dive into YOUR empty slot → upload once → the template (real editor timeline) → TEMPLATE / videos burst
  out → YouTube link → clips (Slice) → three different videos, same song → Autopilot posting 20 a day → pull back: your slot is full.
- Numbers (updated v6, limits changed 10-06): "20 a day" = 2 accounts × 10 a day, true on ELITE only (10 accounts, 10 a day each,
  1,000 a month; 20 × 30 = 600 fits). Pro is now 5 a day / 3 accounts / 100 a month; Creator 1 a day / 1 account / 30. Never print Pro
  with these numbers, 30 a day, or any trial-reel count. End stat: "Autopilot · up to 1,000 posts a month" (loya 10-06).
- Real UI only: createFlow dropzone; the editor timeline is Timeline Glass rebuilt from TraditionalTimeline/glass.ts/cutMarkerStyle.ts with
  goodbye's real words, 33 cut markers, bpm 129 and the song's real waveform (pipeline/tpl-data.json; nothing typed by hand); the Slice
  window (components/remix/slice, assets/ui/slice: real 73-scene run of youtu.be/bruGznwB4Js, 40 kept); the Autopilot setup sentence,
  account switches and Reels phone (components/autopilot). Handles are loya's: @loya.phase3, @loya.wav. Avatars show initials (the app's
  fallback when IG pictures expire).
- "worry" is printed all lowercase on every template chip (loya 10-06 on v3: "fix the template to say 'worry' instead of 'worrY'"; this overrides the old "leave it" ruling). Fixed in the ad's copy of the template data (pipeline/tpl-data.json, pipeline/goodbye-template.json). Presets whose look is all-caps (Overdrive, Airplay) still set it as WORRY: that is the preset's case style, not the typo.
- The YouTube link is the one used for Slice's live test and the earlier "song in videos out" ad (Spider-Man Homecoming shots).
- No preset with its own white/coloured wash anywhere (footage_check). No Tiled Wave. No I'M FINE flip.
- Sung vocal plays under every lyric video: one window 21.12 → end (the three videos, the Reels phone, your video in the slot).
  The narrator ducks it. "Hoe" is sung under the Autopilot scene (it's the song; never shown — the renders keep it disabled).
- The three proof videos re-cut on the measured beat grid every 2 beats (the template's own markers sit on eighth notes).
- Pace: the three videos (busy by nature: fast-cut lyric renders) are the one payoff picture: pace-allow 21.1–24.1. The hook's
  rush flag (0–5.1) is expected (story hook). The body alone measures 59% calm, longest rush 3.3 s.
- Labels on the three videos are the app's real preset names + the footage source (your own shoot / LYRC stock / clips from that YouTube link).
- Length: the brief for this ad says ~30–35 s (it's 34.6, ending as the song's "lie" dies). The old "≤32 s" ruling was for the Rollout cut.
- "That template is what lets you post that much" STAYS: the brief requires saying the template is what makes the volume possible.
- Stock: LYRC's AWE / ROOFTOP SUNRISE / PEACE / LONGING / HEARTBREAK stock folders are AI b-roll (Seedance batches) → banned in ads
  (loya 10-05). Every lyric video in the BODY uses real footage only: loya's day shoot (2026-08-17 Intro Video), his night shoot
  (2026-09-04 Night Car, 2026-08-25 Night Shoot) and the clips LYRC cut from the YouTube link. (The hook's wall still is loya-approved and unchanged
  except the one Tiled Wave tile, now a Night Car Overdrive render.)
- Inside your slot the product screens sit on a lit stage (floor/ceiling grid + light shafts), not a blurred photo.

## AUTOPILOT trial 1 v2 (10-06, loya on trial 1: "dude thats fucking unbelievable") — keep everything he didn't name
- WORSE always reads (his note 1): band heads upright, one size, 190 px apart, dark-edged; they drop in formation; the E
  stumbles but its letter counter-turns; on BLOW UP the band GROWS (×1.75) on a clear dark field in the stadium instead
  of being launched apart. Never scatter, tilt or overlap those five letters.
- The jaw-drop guy is SOLID (note 2): opaque white head, blue cap, hoodie, real cartoon eyes (whites + blue pupils), a jaw
  that drops open in notches as each of the rival's videos lands, his phone in hand. No see-through outlines.
- ONE screen for jaw drop + THEY DID (note 3), 2.9–4.46: HERE'S WHAT / THEY DID on top, the rival's wall building in the
  middle, our artist + the rival at the bottom, "that YOU" in the empty slot. Then the slam: DIDN'T on the real wall.
- DIDN'T is short (note 4): it lands 4.46, leaves 4.96; the camera is already moving in. The body voice starts at 5.25
  ("They" 0.27 s after "didn't" ends; was 0.64 s). The hook take wh-t3 and the song are unchanged (no re-edit needed:
  the body's music hits were kept, only the first line moved). The whole-ad pace rush flag now runs 0–6.2 s (the
  hook + this tighter exit); the body after it passes.
- Movie clips (note 5): Spider-Man kept. The Slice library's 40 clips (the ones LYRC cut from that link, loya's
  "Amazing Shots of SPIDER-MAN HOMECOMING" folder) PLAY in the grid on "clips" (assets/footage/ap-grid.mp4,
  pipeline/grid_mosaic.py); the "clips from that YouTube link" video cuts to a new Spider-Man clip on every beat
  (pipeline/spec-sm03.json → ap-sm3.mp4, 9 clips). Only clips from that one link, so the label stays true.
- Autopilot gets ~5.3 s (note 6): 26.64–31.95; it keeps posting (a 4th post goes out, back on @loya.phase3: rail,
  setup line and handle follow). The end card starts 31.95 (comment lyric 32.24); ad length unchanged, 34.6 s.
- Round 3 (critic r2's fixes, pipeline/ap2/apply_v2_r4.py):
  - 20 = 10 + 10: each account's "10" lifts out of the setup sentence's own "10 lyric videos" (the real SetupSentence is per account)
    as that account switches on; the two meet as 10 +10 and become 20 A DAY; "10 a day × 2 accounts" lands at 29.0.
  - "They posted it": six posts slam onto their wall 5.32–6.62 (z 1000; the old z 1400 tile sat on the camera plane = a black flash at 6.6, fixed).
  - The 16–17 burst grid is cut. TEMPLATE lands on the timeline and whips straight to the Slice window (16.08).
  - Slice is cropped for the phone (title ×1.9 → link field ×2.5 → Find scenes ×2.5 → counter + strip ×1.75), then the 40 clips from that link
    fill the frame as a 5 × 8 playing grid on "clips" (assets/footage/ap-grid58.mp4, re-tiled from ap-grid.mp4 by pipeline/grid_retile.py).
  - The three videos: 2.31 s each, 5 beats of the measured grid (20.206 / 22.516 / 24.826 → 27.136). v1 re-rendered 2 beats earlier
    (spec-ap-v1b → ap-v1b.mp4, same Uplift look + day shoot). The sung vocal window now starts 20.17. Autopilot 27.1 → 31.95 (4.85 s).
  - The timeline ruler sits on the song's downbeat (the app's beatGrid.downbeat; measured hit at template 4.592). The four visible markers
    land one by one on the song's eighths (13.26/13.49/13.73/13.96) and each lights the waveform under it. Lyric chips no longer fly through the ruler; the
    slot lane stays hidden until the slots split in (no empty bar).
  - The filled slot holds lit ~0.65 s before the CTA ("comment lyric for the link" starts 32.75).
  - footage_check's flag on ap-yours2 (0–1 s) is the Spider-Man clip's overcast sky (real footage), not a preset background.

## AUTOPILOT trial 1 v4 (10-06, loya's 7 notes on v3) — keep everything he didn't name
- Audio stays the v3 mix (ElevenLabs narration untouched; pipeline/words-ad-ap4.json = ap3's words). Only SFX moved (pipeline/events-ap4.json,
  mix-ap4.sh → final-mix-ap4.wav): marker snaps on the new playhead landings, the card burst under the posting flurry (6.3), a second impact on 20 (7.23).
- 5.2–8.1 "They posted it. Twenty times a day." is the POSTING CLOCK: a 24-hour dial in the centre of the frame, their real lyric-video tiles
  (only the wall's real-footage tiles, never its stock tiles) fire out of the counter and land round the dial at their hour, faster and faster
  (the day runs power1.in: first post lands on BASS IN 5.86, the 20th on the 7.26 hit); the arc and a sun dot fill the day; the counter climbs
  0 → 20 in the middle; A DAY lands under it on her words. The old six slams + "20 A DAY" parked at the top are gone.
- Words are never parked at the top of the frame (STYLE.md). TEMPLATE now lands in a gap the timeline's lanes open in the frame's centre.
- Hand-off 8.08 → 9.0: the clock flies past the lens while the camera dives into the empty slot; the dropzone grows out of the slot in the
  same push (no drop from above, no pop before the transition covers the frame).
- WORSE heads: each letter sits on a short neck (its bottom meets the neck's top); arms flap and cheer below the letters (v4: -62/-72°).
- The template beat: the playhead (TraditionalTimeline's 2 px line; its ticking time pill is left out for calm) runs one continuous eased
  sweep, template 2.45 → 6.65 s over 10.3 → 16.3 (sine.out); each word and each real cut marker lands the moment the playhead reaches it, so
  markers start at 10.56, while "Lyric times your lyrics" is being said.
- The three proof videos are ALL clips LYRC extracted from YouTube links in loya's library (no more day/night shoot): Interstellar (Uplift),
  Tron: Legacy (Overdrive), Spider-Man Homecoming (Airplay). Labels: "<preset> / clips from a YouTube link". Interstellar and Tron are loya's
  own extracted folders (1080p sources, pipeline/spec-v4-v1.json, spec-v4-v2.json); Spider-Man = that link's Slice run (unchanged).
- Pace: the template's continuous flow and the posting flurry are loya's asks; they make those stretches read busy on pace_check (the
  whole-ad calm drops from 41% to 33%; the rush flag from the hook now runs to 8.9 s). The fill flag at 18.75–19.75 (Slice counter) was in v3 too.

## AUTOPILOT trial 1 v5 (10-06, loya on v4: "dude so much better. now just fix the framing on the youtube clip extraction ones" + the hook's
## "than YOURS / BLOW UP": "could just be cleaner. doesnt need to be that fast cutting... looks super fuckin jumbled") — ONLY these two parts changed
- Audio = final-mix-ap3.wav (ElevenLabs voice), unchanged. Everything outside 1.5–3.0 and 16.1–20.3 is v4.
- Hook 1.5–2.9 (pipeline/ap2/hook_patch.py patch_v5): the couch-footage slab is gone. "a song" clears (1.52), one small framed glimpse
  of HIS song (his couch footage, 440x330 card, blue rim) lands above the band, "than" + "YOURS" under it; nothing crosses the band's
  heads. BLOW UP = ONE move: the camera pulls back while the band grows (WORSE heads exactly as v4), three layers: BLOW UP on top, the band
  in the middle on a dark field, a calm dark crowd (solid silhouettes, a few phone lights) along the bottom only. No ring burst, no white
  flash, no UP trail, no beam swing, no screen push.
- Slice 16.1–20.3 (pipeline/ap2/body.js S4): every framing is the WHOLE Slice window centred in the slot's room (x1.08 arriving → x1.2
  on the link field → x1.2 re-centred on the counter + strip), 24 px clear of each frame edge, so nothing is cut. The window's small print
  is set to read on a phone (ad copy only: 19–20 px ×1.2); the drop zone's fine print is left out (not part of the story). The room's
  ceiling grid now shows over the window (#slCeil; the slot's own ceiling never rendered → the "dead band"). On "clips" the window dims and
  the 40 kept clips spread out of the strip into a 4 x 10 grid that fills the frame edge to edge (assets/footage/ap-grid410.mp4,
  pipeline/grid_retile410.py), then the same whip into Overdrive. The window never zooms out (pulse_check read that as a bump).
- pulse_check: 7 isolated bumps (0.13, 4.67, 8.2, 20.93, 22.73, 26.4, 33.07), same as v4, all in unchanged parts; the count rule (>4)
  flagged v4 too. No repeating pairs.

## AUTOPILOT trial 1 v6 (10-06, loya on v5: "thats so fucking fire bro. fix the autopilot copy at the end thats not accurate. and for the
## third vid use a diff lyric preset like redline") — ONLY these two changed
- End card #eStat: "Autopilot · up to 1,000 posts a month" (was "Autopilot on Pro · 10 a day per account", false since the 10-06 limits).
  The narration's "twenty a day", the "10 a day × 2 accounts" line and the setup sentence (10 a day, 2 weeks) stay: all true on Elite.
- Third proof video (24.55–27.75, Tron: Legacy clips, also the clip inside the Reels phone) = REDLINE (choreo-redline), a program preset
  rendered through the export's --program-frames path (pipeline/spec-v6-3.json = spec-v4b-3 with the preset swapped → assets/footage/ap-pv3r.mp4).
  Same clips, ins, cut times and lyric span. Label "Redline / clips from a YouTube link". footage_check passes on it.
- Redline's red letters are the product's real output: palette_check's red flag at 25.0 s is allowed.
- Audio = final-mix-ap3.wav, unchanged (transcript identical).
