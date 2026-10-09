# Reference — "make this for my company"

The owner sends an ad they love (an Instagram reel, a TikTok, a competitor's ad, a big brand's launch video) and says
"make this for my company". That's one of the best briefs there is: it shows the energy, pace and idea they want.
It's also the easiest way to make a fake-looking copy. The LYRC build's best whole ad started exactly like this (a
competitor's "it's live" reel → "make this vid but for LYRC") and still followed the rule that came out of it:
*"the only things it should copy are the IDEAS from the example. not the exact song, not the exact designs, not the
exact positionings, not the exact hook."*

## 1. Get the video
- The owner pastes the link (Instagram reel, TikTok, YouTube Short, X post): `ref_breakdown.sh` downloads it with
  yt-dlp. Public posts need no login. A dropped-in video file works too.
- If the link won't download (a private account, a login wall), ask the owner to screen-record it and drop the file in.
  Never ask for their Instagram password or use their browser cookies to get around it.
- Their video is for study only. Never put any of its footage, audio, music, logo, characters or words into the ad.

## 2. Break it down (Claude can't watch an mp4; this makes it readable)
```bash
bash ~/.claude/skills/motion-ad/scripts/ref_breakdown.sh <link or video file> <ad folder>/reference
```
It writes a 0.25 s hook sheet, a 0.5 s whole-video sheet, every hard cut, what's said or sung (Whisper), the music map
and the pace. Read both sheets at full size, then write `reference/breakdown.md`:

### The breakdown
| Part | What to write |
|---|---|
| The hook | the line (words), the device (HOOKS.md → Opening devices), what's on frame 0, when the premise is clear |
| The story | each scene in one line: time range → the JOB it does (problem, the product working, proof, payoff, CTA) |
| The rhythm | cuts per second, where the big moves land on the music, calm vs rush (pace.txt) |
| The look | type treatments, camera language, transitions, how text lives in the layout, palette use |
| Why it works | 3–5 bullets: the thing that would make a stranger stop and watch |
| What it gets wrong | anything that breaks our rules (fake UI, unverifiable claims, pulsing to the beat, dead gaps): don't inherit it |

## 3. Transfer it to this business
Write a transfer table in `decisions.md` before building anything:

| Their beat | Its job | Our version (this business's real product, proof, customer) |
|---|---|---|
| e.g. 0–2 s: a phone buzzing with orders | the stake: demand | our real booking screen filling up, real count from claims.md |

Then build with the normal build order (SKILL.md), from step 2. What carries over from the reference:
- the IDEA of each beat, the story shape, the energy and pace, the kind of hook device, the kind of camera move.
What never carries over:
- their footage, music, words, hook line, exact layouts and positions, characters, logos, colors (ours come from
  brand.json), and any claim that isn't true for this business.

## 4. Before delivery, check it isn't a copy
- Put the two hook sheets side by side. If a stranger would call ours "the same ad with a new logo", change the
  layouts, the hook's visual and the words until they wouldn't.
- Every claim is ours and verified (claims.md). Their numbers mean nothing for this business.
- In the delivery message, say in one line what was taken from the reference (the idea) and what's new.
