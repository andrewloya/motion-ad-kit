# LYRC in Claude — hook plan

Reference (loya, 10-02): invideo's MCP launch reel (Dd_tLbHOTep, 48 s, music only). Ideas taken from it, not designs:
an agent drives the real editor from a chat; you type plain words, the work happens; you change it with more words;
one more ask gives you a batch; it closes on "it's live now". Our version: LYRC's connector inside Claude.

Gate (checked 10-02): the connector is open to every LYRC account (custom connector in Claude; Claude needs a paid plan
for custom connectors, per our own settings page). Claude's directory listing and the ChatGPT plugin are still in review,
so the ad names Claude only. 31 payers have ever used it (feature X-ray 09-28), so this ad is discovery, not a reminder.
Export is paid; watching the preview is free (the widget's own footnote). Nothing in the ad says "free".

Song: clovers (out 2025-10-03), master revC (+8 bpm). Ad 0 = song 1.82, the +50 dB hit.
Measured (ad time): 0.00 hit · 1.14 hit · 1.82 bass in · 2.90–3.62 SILENCE · 3.62 +49 dB hit (HOOK_END) · 6.53 vocal
"A heavy heart…" · 10.46–10.90 silence → hit · 12.02–12.72 silence → +47 dB hit · 13.74 "I'll give you one more night…" ·
17.76–18.16 silence → hit · 23.64 bass in · 25.00–25.44 silence → hit · 30.92 bass in.

## 6 ideas (line × device × visual), scored 1–5
Criteria: value / loop / stranger / thumb / premise / stake / double-take / visual surprise / payoff / real.

| # | Line | Device | Visual | Score |
|---|---|---|---|---|
| **1 ✓** | stop editing lyric videos. **text Claude.** (built first as "text them.") | the crush (new) | A dense editor timeline (real night-shoot thumbs, the song's real waveform, keyframes) on a tilted plane; STOP EDITING lands on it; on the bass the timeline is crushed, track by track, into one chat bubble; TEXT THEM. lands in the silence; the bubble sends on the hit | 5/4/5/4/5/5/4/5/5/4 = **46** |
| 2 | type one sentence. get 4 different lyric videos. | counter / number slam | the sentence's letters fly apart into four frames that become four real renders | 5/3/5/4/5/5/3/4/5/4 = 43 |
| 3 | lyric videos are a text message now. | result first + pull-back | a real render full-bleed, the camera pulls back hard and it's a card inside a chat under one message | 4/4/4/4/4/4/4/4/5/5 = 42 |
| 4 | Claude can make your lyric videos now. | cold open on the product | the Claude composer huge, the ask typing itself with a caret, send | 4/4/3/3/4/4/4/2/5/5 = 38 |
| 5 | if you can text, you can make a lyric video. | lock-screen POV | a "your video is ready" notification lands on a lock screen (cover-art ad already used a lock screen) | 4/4/4/3/4/4/3/3/4/4 = 37 |
| 6 | you've spent more time editing your lyric video than writing the song. | split screen | an editor clock spinning vs a chat; unverifiable for many viewers | 3/4/4/4/3/5/5/3/3/3 = 37 |

Pick: #1. A stranger gets "I can stop editing" in a second and can't yet say how ("text who?"). The picture isn't
the literal one (a chat) until the crush turns the old way INTO the new way. It aims at editing in general, never at
LYRC's own editor (the timeline is a generic NLE, not LYRC's).

## Storyboard (0–3.62, every 0.25 s)
Layers: back = the timeline plane (tilted, perspective) · mid = type · front = grain + foreground keyframe diamonds.
Type voices: Archivo (STOP EDITING, TEXT THEM.) + Space Grotesk (lyric videos.).

| t | picture | type | sound |
|---|---|---|---|
| 0.00 | timeline plane braking out of a whip (blur decaying), playhead red, thumbs lit | STOP EDITING letters mid-flight from the camera, huge | +50 dB hit + whoosh |
| 0.25 | plane settles into its tilt, playhead scrubbing | letters hit the plane: squash + width punch, staggered | thumps per letter |
| 0.50 | slow drift right (calm) | STOP EDITING holds | |
| 0.75 | drift | "lyric videos." rises from its mask under it | tick |
| 1.00–1.75 | drift; playhead crosses cut markers that STAY lit | all three read | 1.14 small hit |
| 1.82 | BASS IN: anticipation — the tracks bulge apart (scaleY 1.06) | words lift with the plane | low thump |
| 2.05–2.75 | the crush: tracks slam together one by one (back.in), the plane squeezes to a rounded pill, colours drain to cream | EDITING gets crushed flat with it (scaleY → 0), STOP falls away | crunch + whoosh |
| 2.90 | SILENCE: the pill IS a chat bubble, cream, tilted flat to the camera with an overshoot | TEXT THEM. lands above it (mass land, per-letter) | silence, one soft tick |
| 3.00–3.50 | the bubble's words type in fast (the ask) | TEXT THEM. holds (~0.7 s alone, 1.0 s total) | typing ticks |
| 3.62 | +49 dB hit: the bubble SENDS — whips up, camera pulls back into Claude's chat | TEXT THEM. carries up with the bubble, gone by 4.1 | hit + send whoosh |
